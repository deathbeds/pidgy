from pathlib import Path
from textwrap import indent
import oauthlib
import tomli
import sys

MAIN = __name__ == "__main__"
IN = " " * 2
HERE = Path(__file__).parent
SUITE = HERE / "tests.toml"

data = tomli.loads(SUITE.read_text())

if MAIN:
    body = """# `pidgy` test suite \n\n"""
    for i, (anchor, test) in enumerate(data.items(), 1):
        input, output, description = (
            test.get("in", ""),
            test.get("out", ""),
            test.get("description", ""),
        )
        input = indent(input, IN)
        output = indent(output, IN)
        body += f"""## {description or anchor.replace(*'- ')}\n\n"""
        body += indent(f"""### Markdown Input {i}\n\n{input}\n""", IN)
        body += indent(f"""### Python Output {i}\n\n{output}\n""", IN)

    Path(HERE / "formatted_tests.md").write_text(body)
