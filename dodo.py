"""dodo.py"""
from inspect import getsource
from pathlib import Path
from re import sub
import shutil
from textwrap import dedent
from hashlib import sha256
import sys

import doit.tools

PY = Path(sys.executable)
DOIT_CONFIG = dict(verbosity=2)
HERE = Path(__file__).parent
CONF = HERE / "conf.py"
DIST = HERE / "dist"
DOCS = HERE / "docs"
LITE = HERE / "lite"
SHA256SUMS = DIST / "SHA256SUMS"
WHL_DEPS = [
    "pyproject.toml",
    "readme.md",
    "setup.cfg",
    "setup.py",
    *Path("src").rglob("*.py"),
    *Path("src/pidgy/kernel/pidgy").rglob("*"),
]


def task_dist():
    """build distributions"""

    def hashfile():
        lines = []

        for p in sorted([*DIST.glob("pidgy*.whl"), *DIST.glob("pidgy*.tar.gz")]):
            if p == SHA256SUMS:
                continue
            lines += ["  ".join([sha256(p.read_bytes()).hexdigest(), p.name])]

        output = "\n".join(lines)
        print(output)
        SHA256SUMS.write_text(output)

    yield dict(
        name="pidgy",
        doc="build pidgy distributions",
        file_dep=WHL_DEPS,
        actions=[
            lambda: [shutil.rmtree(DIST) if DIST.is_dir() else None, None][-1],
            [PY, "setup.py", "sdist"],
            [PY, "-m", "pip", "wheel", "-w", DIST, "--no-deps", "."],
            hashfile,
        ],
        targets=[SHA256SUMS],
    )


@doit.create_after("dist")
def task_lite():
    """build jupyterlite site and pre-requisites"""
    wheel = sorted(DIST.glob("pidgy*.whl"))[-1]

    yield dict(
        name="wheels",
        file_dep=[SHA256SUMS, wheel],
        actions=[
            (doit.tools.create_folder, [LITE / "pypi"]),
            doit.tools.CmdAction(
                [PY, "-m", "pip", "download", "--prefer-binary", wheel],
                cwd=str(LITE / "pypi"),
                shell=False,
            ),
        ],
    )

    yield dict(
        name="build",
        file_dep=[
            SHA256SUMS,
            wheel,
            LITE / "jupyter_lite_config.json",
            *DOCS.rglob("*.ipynb"),
        ],
        actions=[
            doit.tools.CmdAction(
                [PY, "-m", "jupyter", "lite", "archive"], cwd=str(LITE), shell=False
            )
        ],
        targets=[LITE / "output/SHA256SUMS"],
    )


@doit.create_after("lite")
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
