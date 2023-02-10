"""a mkdocs plugin for pidgy

pidgy is designed to decouple input from output. input is a template for the output.
as a result we want to suppress the inputs, but still make that accessible for an eager reader.

mkdocs is designed for markdown so convert notebooks directly to markdown 
and try mkdocs into things notebooks are standard content"""

import nbconvert, re
import functools, re
import mkdocs
from pathlib import Path

PIDGY = re.compile(r"\s*%(re)?load_ext pidgy")
# https://tonyfast.github.io/tonyfast/xxii/2022-12-31-markdownish-notebook.html#generating-the-template

HEAD = """{% from 'base/jupyter_widgets.html.j2' import jupyter_widgets %}
<script src="{{ resources.require_js_url }}"></script>
{{ jupyter_widgets(resources.jupyter_widgets_base_url, resources.html_manager_semver_range, resources.widget_renderer_url) }}
"""
HERE = Path(__file__).parent

mkdocs.utils.markdown_extensions += (".ipynb",)
# dont tell nobody, but now mkdocs things notebooks are valid content


class PidgyExporter(nbconvert.exporters.HTMLExporter):
    def from_notebook_node(self, nb, resources=None, **kw):
        resources = self._init_resources(dict(is_pidgy=is_pidgy(nb)))
        return super().from_notebook_node(nb, resources, **kw)


class Notebooks(mkdocs.plugins.BasePlugin):
    exporter_cls = PidgyExporter
    config_scheme = (
        # ('foo', mkdocs.config.config_options.Type(str, default='a default value')),
    )

    @functools.lru_cache
    def get_exporter(self, key="mkdocs", **kw):
        kw.setdefault("template_file", key)
        exporter = self.exporter_cls(**kw)
        exporter.environment.filters.setdefault("attachment", replace_attachments)
        from jinja2 import DictLoader

        for loader in exporter.environment.loader.loaders:
            if isinstance(loader, DictLoader):
                loader.mapping[key] = (HERE / "templates" / "ipynb.md.j2").read_text()
                loader.mapping["HEAD"] = HEAD
                break
        return exporter

    def on_page_read_source(self, page, config):
        import nbformat.v4
        import json

        if page.file.is_modified():
            if page.file.src_uri.endswith((".ipynb",)):
                body = Path(page.file.abs_src_path).read_text()
                nb = nbformat.v4.reads(body)
                exporter = self.get_exporter()
                return "\n".join(
                    (
                        "---",
                        json.dumps(nb.metadata),
                        "---",  # add metadata as front matter
                        exporter.from_notebook_node(nb)[0],
                    )
                )

    def on_post_page(self, output, page, config):
        if '<script type="application/vnd.jupyter.widget-view+json">' in output:
            left, sep, right = output.partition("</head")
            exporter = self.get_exporter()
            return (
                left
                + self.get_exporter()
                .environment.get_template("HEAD")
                .render(
                    resources=dict(
                        jupyter_widgets_base_url=exporter.jupyter_widgets_base_url,
                        html_manager_semver_range=exporter.html_manager_semver_range,
                        widget_renderer_url=exporter.widget_renderer_url,
                        require_js_url=exporter.require_js_url,
                    )
                )
                + sep
                + right
            )

    def on_page_markdown(self, markdown, page, config, files):
        import markdown

        title = markdown.Markdown(extensions=config["markdown_extensions"]).convert(page.title)
        page.title = title[len("<p>") : -len("</p>")].strip()


def is_pidgy(nb):
    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            if PIDGY.match("".join(cell["source"])):
                return True
    return False


def replace_attachments(cell):
    source = "".join(cell["source"])
    if cell.get("attachments"):
        for k, v in cell["attachments"].items():
            for t, v in v.items():
                source = source.replace("attachment:" + k, "data:" + t + ";base64," + v)
    return source
