from argparse import ArgumentParser
from sys import argv

from importnb import Notebook

from .tangle import Tangle
from .weave import Weave

parser = ArgumentParser()
parser.add_argument("file")


def main():
    from .loader import Literate

    ns = parser.parse_args(argv[1:])
    module = Literate.load(ns.file)
    from rich import print
    from rich.markdown import Markdown

    print(Markdown(module._repr_markdown_()))


if __name__ == "__main__":
    main()
