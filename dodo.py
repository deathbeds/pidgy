"""dodo.py"""
from pathlib import Path
from re import sub
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
LICENSE = HERE / "LICENSE"
EXT = LITE / "jupyterlite-pidgy"
LITE_REQS = LITE / "requirements.txt"
LITE_PYPI = LITE / "pypi"
LITE_PYPI_SHA256SUMS = LITE_PYPI / "SHA256SUMS"
LITE_SHA256SUMS = LITE / "_/_/SHA256SUMS"
EXT_LICENSE = EXT / LICENSE.name
EXT_SRC_PKG = EXT / "package.json"
EXT_SRC_PKG_DATA = json.load(EXT_SRC_PKG.open())
EXT_DIST_PKG = EXT / "py_src/jupyterlite_pidgy/labextension/package.json"
EXT_DIST = EXT / "dist"
EXT_WHL_NAME = f"""jupyterlite_pidgy-{EXT_SRC_PKG_DATA["version"]}-py3-none-any.whl"""
EXT_WHL = EXT_DIST / EXT_WHL_NAME
EXT_ICON = EXT / "style/pidgy.png"
SHA256SUMS = DIST / "SHA256SUMS"
KERNEL_DATA = HERE / "src/pidgy/kernel/pidgy"
KERNEL_ICON = KERNEL_DATA / "logo-64x64.png"
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
    *KERNEL_DATA.rglob("*"),
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


def build_hashfile(hashfile, get_deps):
    deps = sorted(get_deps())

    if not deps:
        raise Exception(f"no files found to hash for {hashfile}")
    lines = []

    for p in deps:
        lines += ["  ".join([sha256(p.read_bytes()).hexdigest(), p.name])]

    output = "\n".join(lines)
    print(output)
    hashfile.write_text(output)


def task_dist():
    """build distributions"""
    yield dict(
        name="pidgy",
        doc="build pidgy distributions",
        file_dep=WHL_DEPS,
        actions=[
            lambda: [shutil.rmtree(DIST) if DIST.is_dir() else None, None][-1],
            [PY, "setup.py", "sdist"],
            [PY, "-m", "pip", "wheel", "-w", DIST, "--no-deps", "."],
            (
                build_hashfile,
                [
                    SHA256SUMS,
                    lambda: [*DIST.glob("pidgy*.whl"), *DIST.glob("pidgy*.tar.gz")],
                ],
            ),
        ],
        targets=[SHA256SUMS],
    )


def task_labext():
    pkg = EXT / "package.json"
    lock = EXT / "yarn.lock"
    integrity = EXT / "node_modules/.yarn-integrity"
    ts_src = [*(EXT / "src").rglob("*.ts")]
    ts_buildinfo = EXT / "tsconfig.tsbuildinfo"
    pypi = EXT / "pypi/pidgy"
    pypi_ts = EXT / "src/_pypi.ts"

    def _do(*args, **kwargs):
        cwd = str(kwargs.pop("cwd", EXT))
        return doit.tools.CmdAction([*args], **kwargs, cwd=cwd, shell=False)

    def _copy_static():
        src = sorted(DIST.glob("*.whl"))[-1]
        dest = pypi / src.name
        if pypi.exists():
            shutil.rmtree(pypi)
        copy_one(src, dest)
        ctx = "!!file-loader?name=pypi/pidgy/[name].[ext]&context=.!../pypi/pidgy"
        lines = [
            f"""export * as allJSONUrl from '{ctx}/all.json';""",
            f"""export * as pidgyWheelUrl from '{ctx}/{dest.name}';""",
        ]
        pypi_ts.write_text("\n".join(lines))

        copy_one(KERNEL_ICON, EXT_ICON)
        copy_one(LICENSE, EXT_LICENSE)

    yield dict(
        name="yarn",
        file_dep=[pkg] + ([lock] if lock.exists() else []),
        targets=[integrity],
        actions=[_do("jlpm", "--prefer-offline", "--ignore-optional")],
    )

    yield dict(
        name="copy:static",
        file_dep=[*DIST.glob("*.whl"), KERNEL_ICON, LICENSE],
        targets=[pypi / "all.json", pypi_ts, EXT_ICON, EXT_LICENSE],
        actions=[_copy_static, _do("jupyter", "lite", "pip", "index", pypi)],
    )

    yield dict(
        name="lint",
        file_dep=[*ts_src],
        actions=[
            _do("jlpm", "eslint"),
        ],
    )

    yield dict(
        name="build:ts",
        file_dep=[*ts_src, pkg, integrity, pypi_ts],
        targets=[ts_buildinfo],
        actions=[_do("jlpm", "build:lib")],
    )

    yield dict(
        name="build:ext",
        file_dep=[ts_buildinfo, integrity, pkg, pypi_ts, pypi / "all.json"],
        targets=[EXT_DIST_PKG],
        actions=[_do("jlpm", "build:labextension")],
    )

    yield dict(
        name="wheel:ext",
        file_dep=[EXT_DIST_PKG, EXT_LICENSE, SHA256SUMS],
        actions=[_do(PY, "-m", "pip", "wheel", "--no-deps", "-w", EXT_DIST, ".")],
        targets=[EXT_WHL],
    )


def task_lite():
    """build jupyterlite site and pre-requisites"""

    def _wheels():
        if LITE_PYPI_SHA256SUMS.exists():
            LITE_PYPI_SHA256SUMS.unlink()

        wheel = sorted(DIST.glob("pidgy-*.whl"))[-1]

        for old_wheel in LITE_PYPI.glob("pidgy-*.whl"):
            old_wheel.unlink()

        rc = subprocess.check_call(
            [PY, "-m", "pip", "wheel", "--prefer-binary", wheel, "-r", LITE_REQS],
            cwd=str(LITE_PYPI),
        )

        if rc == 0:
            build_hashfile(
                LITE_PYPI_SHA256SUMS, lambda: [*LITE_PYPI.glob("*py3-none-any.whl")]
            )
            return True

        return False

    yield dict(
        name="wheels",
        file_dep=[SHA256SUMS, LITE_REQS, EXT_WHL],
        actions=[(doit.tools.create_folder, [LITE / "pypi"]), _wheels],
    )

    def _lite(args, extra_args=None):
        lite_cmd = [PY, "-m", "jupyter", "lite"]
        lite_args = ["--debug", "--LiteBuildConfig.federated_extensions", EXT_WHL]
        extra_args = extra_args or []
        return doit.tools.CmdAction(
            [*lite_cmd, *args, *lite_args, *extra_args],
            cwd=str(LITE),
            shell=False,
        )

    yield dict(
        name="build",
        file_dep=[
            SHA256SUMS,
            EXT_WHL,
            *LITE.glob("*.json"),
            *(LITE / "retro").glob("*.json"),
            *DOCS.rglob("*.ipynb"),
        ],
        actions=[
            _lite(["build"]),
            _lite(["doit"], ["--", "pre_archive:report:SHA256SUMS"]),
        ],
        targets=[LITE_SHA256SUMS],
    )


@doit.create_after("lite")
def task_docs():
    def post():
        CONF.write_text(
            "\n".join(
                [
                    "import subprocess",
                    """subprocess.call(["doit", "dist"])""",
                    """subprocess.call(["doit", "labext"])""",
                    """subprocess.call(["doit", "lite"])""",
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
            LITE_SHA256SUMS,
        ],
        actions=["sphinx-build . _build/html %(pos)s"],
        pos_arg="pos",
        targets=[HERE / "_build/html/.buildinfo"],
    )


def copy_one(src, dest):
    if not src.exists():
        return False
    if not dest.parent.exists():
        dest.parent.mkdir(parents=True)
    if dest.exists():
        if dest.is_dir():
            shutil.rmtree(dest)
        else:
            dest.unlink()
    if src.is_dir():
        shutil.copytree(src, dest)
    else:
        shutil.copy2(src, dest)
