import json
from pathlib import Path
import logging
from os import environ, system
from sys import executable
from subprocess import check_output
from shutil import copy

ROOT = Path(__file__).parent.parent
LOGO = ROOT / "pidgy.png"
DOCS = ROOT / "docs"

log = logging.getLogger("mkdocs")


def on_pre_build(config):
    if not (DOCS / LOGO.name).exists():
        log.info("move logo to docs dir")
        copy(LOGO, DOCS)


def on_post_build(config):
    if "READTHEDOCS" in environ:
        C = ROOT / "lite" / "jupyter_lite_config.json"
        data = json.loads(C.read_text())
        data["LiteBuildConfig"]["output_dir"] = str(Path(config.site_dir) / "run")
        C.write_text(json.dumps(data))
        log.info("building lite")
        check_output([executable, "-m", "doit", "lite"], cwd=ROOT)


# https://www.mkdocs.org/user-guide/configuration/#hooks
