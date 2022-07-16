import ast
from pathlib import Path
import pytest
from tomli import loads
from pidgy.tangle import Python, get_renderer

HERE = Path(__file__).parent

TESTS = HERE / "tests.toml"

tests = loads(TESTS.read_text())

renderer = get_renderer()
render = renderer.render

@pytest.mark.parametrize("name,test", list(tests.items()))
def test_compare(name, test):
    input, expected, valid = test.get("in", ""), test.get("out", ""), test.get("valid", True)
    rendered = render(input)
    assert rendered == expected, "the rendered code does not match."
    if valid:
        assert ast.parse(expected), "the expected code is not valid python."