from pathlib import Path
import logging
from os import environ, system
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
        log.info("building lite")
        log.info(check_output(["doit", "lite"], cwd=ROOT)        )


# https://www.mkdocs.org/user-guide/configuration/#hooks
