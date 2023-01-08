from pathlib import Path

from mkdocs_macros.plugin import MacrosPlugin


class PidgyPlugin(MacrosPlugin):
    def on_config(self, config):
        self.config.setdefault("modules", [])
        self.config["modules"].append(__name__)
        super().on_config(config)

    def on_page_read_source(self, page, config):
        with Path(config["docs_dir"], page.file.src_path).open() as file:
            first = next(file, "")
            if first.startswith("#!/usr/bin/env"):
                page.shebang = first
            return "".join(file)


def define_env(env):
    pass


def on_pre_page_macros(self):
    if self.page.file.src_path.endswith((".md",)):
        from midgy.run import Markdown

        if getattr(self.page, "shebang", None):
            module = Markdown().load_code(self.page.markdown, self.page.file.src_path)
            self.variables.update(vars(module))
