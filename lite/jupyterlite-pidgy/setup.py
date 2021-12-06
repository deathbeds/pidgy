"""jupyterlite-pidgy setup"""
import json
from pathlib import Path

HERE = Path(__file__).parent.resolve()
EXT = HERE / "py_src/jupyterlite_pidgy/labextension"
PKG = EXT / "package.json"

__js__ = json.load(PKG.open())
SHARE = f"""share/jupyter/labextensions/{__js__["name"]}"""

setup_args = dict(
    version=__js__["version"],
    data_files=[
        (SHARE, ["install.json"])
    ] + [
        (f"""{SHARE}/{p.parent.relative_to(EXT).as_posix()}""", [
            str(p.relative_to(HERE).as_posix())
        ])
        for p in EXT.rglob("*") if not p.is_dir()
    ]
)

if __name__ == "__main__":
    import setuptools
    setuptools.setup(**setup_args)
