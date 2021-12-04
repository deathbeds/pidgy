"""dodo.py"""
from pathlib import Path
from re import sub
import shutil
from hashlib import sha256
import sys
import os
import subprocess

import doit.tools

PY = Path(sys.executable)
DOIT_CONFIG = dict(verbosity=2)
DODO = Path(__file__)
HERE = DODO.parent
CONF = HERE / "conf.py"
DIST = HERE / "dist"
DOCS = HERE / "docs"
LITE = HERE / "lite"
SHA256SUMS = DIST / "SHA256SUMS"
WHL_PY = [
    "setup.py",
    *Path("src").rglob("*.py"),
]
WHL_MD = ["readme.md", Path("src/pidgy/readme.md")]
WHL_DEPS = [
    "pyproject.toml",
    "setup.cfg",
    *Path("src/pidgy/kernel/pidgy").rglob("*"),
    *WHL_MD,
    *WHL_PY,
]
ALL_PY = [DODO, *WHL_PY]
ALL_MD = [*WHL_MD]
SOURCE_DATE_EPOCH = (
    subprocess.check_output(["git", "log", "-1", "--format=%ct"])
    .decode("utf-8")
    .strip()
)
os.environ.update(SOURCE_DATE_EPOCH=SOURCE_DATE_EPOCH)


def task_lint():
    """apply source formatting"""
    yield dict(name="black", file_dep=ALL_PY, actions=[["black", *ALL_PY]])
    yield dict(name="md", file_dep=ALL_MD, actions=[["mdformat", *ALL_MD]])


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
                [PY, "-m", "pip", "wheel", "--prefer-binary", wheel],
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
        targets=[LITE / "_/_/SHA256SUMS"],
    )


@doit.create_after("lite")
def task_docs():
    def post():
        CONF.write_text(
            "\n".join(
                [
                    "import subprocess",
                    """subprocess.check_call(["doit", "lite"])""",
                    sub(
                        r'external_toc_path = "\S+_toc.yml"',
                        r'external_toc_path = "_toc.yml"',
                        CONF.read_text(),
                    ),
                ]
            )
        )

    yield dict(
        name="sphinx-config",
        file_dep=["_toc.yml", "_config.yml"],
        actions=[
            "jb config sphinx .",
            post,
            "black conf.py",
        ],
        targets=[CONF],
    )

    yield dict(
        name="sphinx-build",
        file_dep=[CONF, *DOCS.rglob("*.ipynb")],
        actions=["sphinx-build . _build/html %(pos)s"],
        pos_arg="pos",
        targets=[HERE / "_build/html/.buildinfo"],
    )