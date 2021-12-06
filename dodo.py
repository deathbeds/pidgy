"""dodo.py"""
from json import encoder
from pathlib import Path
from re import L, sub
import shutil
from hashlib import sha256
import sys
import os
import subprocess
import json

import doit.tools

PY = Path(sys.executable)
DOIT_CONFIG = dict(verbosity=2)
DODO = Path(__file__)
HERE = DODO.parent
CONF = HERE / "conf.py"
DIST = HERE / "dist"
DOCS = HERE / "docs"
LITE = HERE / "lite"
EXT = LITE / "jupyterlite-pidgy"
EXT_DIST = EXT / "py_src/jupyterlite_pidgy/labextension/package.json"
SHA256SUMS = DIST / "SHA256SUMS"
WHL_PY = [
    p
    for p in [
        HERE / "setup.py",
        *Path("src").rglob("*.py"),
    ]
    if p.name != "_version.py"
]
WHL_MD = [HERE / "readme.md", Path("src/pidgy/readme.md")]
WHL_DEPS = [
    HERE / "pyproject.toml",
    HERE / "setup.cfg",
    *Path("src/pidgy/kernel/pidgy").rglob("*"),
    *WHL_MD,
    *WHL_PY,
]
ALL_PY = [DODO, *WHL_PY]
ALL_MD = [*WHL_MD]
ALL_JSON = [
    *LITE.glob("*.json"),
    *LITE.glob("*/*.json"),
    *[p for p in WHL_DEPS if p.suffix == "json"],
]
SOURCE_DATE_EPOCH = (
    subprocess.check_output(["git", "log", "-1", "--format=%ct"])
    .decode("utf-8")
    .strip()
)
os.environ.update(SOURCE_DATE_EPOCH=SOURCE_DATE_EPOCH)


def task_lint():
    """apply source formatting"""
    yield dict(name="black", file_dep=ALL_PY, actions=[["black", *ALL_PY]])

    for a_json in ALL_JSON:
        yield dict(
            name=f"json:{a_json.relative_to(HERE)}",
            file_dep=[a_json],
            actions=[
                lambda: a_json.write_text(
                    json.dumps(
                        json.loads(a_json.read_text(encoding="utf-8")),
                        indent=2,
                        sort_keys=True,
                    )
                    + "\n",
                    encoding="utf-8",
                )
                > 0
            ],
        )


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
def task_labext():
    pkg = EXT / "package.json"
    lock = EXT / "yarn.lock"
    integrity = EXT / "node_modules/.yarn-integrity"
    ts_src = [*(EXT / "src").rglob("*.ts")]
    ts_buildinfo = EXT / "tsconfig.tsbuildinfo"

    def do(*args, **kwargs):
        cwd = str(kwargs.pop("cwd", EXT))
        return doit.tools.CmdAction([*args], **kwargs, cwd=cwd, shell=False)

    yield dict(
        name="yarn",
        file_dep=[pkg, lock],
        targets=[integrity],
        actions=[do("jlpm", "--prefer-offline", "--ignore-optional")],
    )

    yield dict(
        name="build:ts",
        file_dep=[*ts_src, pkg, integrity],
        targets=[ts_buildinfo],
        actions=[do("jlpm", "build:lib")],
    )

    yield dict(
        name="build:ext",
        file_dep=[ts_buildinfo, integrity, pkg],
        targets=[EXT_DIST],
        actions=[do("jlpm", "build:labextension")],
    )


@doit.create_after("labext")
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
            EXT_DIST,
            *LITE.glob("*.json"),
            *(LITE / "retro").glob("*.json"),
            *DOCS.rglob("*.ipynb"),
        ],
        actions=[
            doit.tools.CmdAction(
                [PY, "-m", "jupyter", "lite", "build"], cwd=str(LITE), shell=False
            )
        ],
        targets=[LITE / "_/_/jupyter-lite.json"],
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
        file_dep=[
            CONF,
            *DOCS.rglob("*.ipynb"),
            *(HERE / "_templates").glob("*.html"),
            LITE / "_/_/jupyter-lite.json",
        ],
        actions=["sphinx-build . _build/html %(pos)s"],
        pos_arg="pos",
        targets=[HERE / "_build/html/.buildinfo"],
    )
