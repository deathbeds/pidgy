"""dodo.py"""
from inspect import getsource
from pathlib import Path
from re import sub
from textwrap import dedent

from doit.tools import config_changed

CONF = Path("conf.py")
DOIT_CONFIG = dict(verbosity=2)


def task_docs():
    def write_addon():
        def setup(app):
            def on_config_inited(app, error):
                try:
                    __import__("jupyterlite")
                except (ImportError, AttributeError):
                    print("jupyterlite not available, no big")
                    return

                from subprocess import check_call

                wheel = ["pip", "wheel", "--w=dist", "--no-deps"]
                check_call([*wheel, "."])
                check_call([*wheel, "htmlmin"])
                check_call(["jupyter", "lite", "build"], cwd="lite")

            app.connect("config-inited", on_config_inited)

        CONF.write_text(dedent(getsource(setup)))

    def post():
        CONF.write_text(
            sub(
                r'external_toc_path = "\S+_toc.yml"',
                r'external_toc_path = "_toc.yml"',
                CONF.read_text(),
            )
        )

    yield dict(
        name="sphinx-config",
        actions=[
            write_addon,
            "jb config sphinx . >> conf.py",
            "black conf.py",
            post,
        ],
        targets=[CONF],
    )
    yield dict(
        name="sphinx-build",
        actions=["sphinx-build . _build/html %(pos)s"],
        pos_arg="pos",
    )
