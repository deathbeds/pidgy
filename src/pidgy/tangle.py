"""tangle.py provides the Markdown to Python translation model.
"""
from io import StringIO
from urllib.parse import urlparse

from midgy.python import Python

# an instance of this class is used to transform markdown to valid python
# in the ipython extension. the python conversion is constrained by being
# a line for line transformation using indent code blocks (not code fences)
# as references for translating the markdown to valid python objects.

class IPython(Python):
    URL_PROTOCOLS = "file", "http", "https"
    VALID_URL_LIST_TOKENS = {
        "paragraph_open",
        "paragraph_close",
        "bullet_list_open",
        "bullet_list_close",
        "list_item_open",
        "list_item_close",
    }

    def _get_url_list(self, tokens):
        urls = []
        for token in tokens:
            if token.type in self.VALID_URL_LIST_TOKENS:
                continue
            elif token.type == "inline":
                for line in StringIO(token.content):
                    parsed = urlparse(line)
                    if parsed.netloc in self.URL_PROTOCOLS:
                        urls.append(line.strip())
                        continue
                    break
                else:
                    continue
                break
            break
        else:
            return urls


def load_ipython_extension(shell):
    from traitlets import Instance

    def tangle(line, cell):
        print(shell.tangle.render(cell))

    def parse(line, cell):
        print(shell.tangle.parse(cell))

    shell.add_traits(tangle=Instance(IPython, ()))
    shell.input_transformer_manager.cleanup_transforms.insert(0, shell.tangle.render_lines)
    shell.register_magic_function(tangle, "cell")
    shell.register_magic_function(parse, "cell")


def unload_ipython_extension(shell):
    if shell.has_trait("tangle"):
        shell.input_transformer_manager.cleanup_transforms = list(
            filter(
                shell.tangle.render_lines.__ne__,
                shell.input_transformer_manager.cleanup_transforms,
            )
        )
