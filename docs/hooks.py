from pathlib import Path
import logging
from os import environ
from shutil import move

ROOT = Path.cwd()
if environ.get("CI"):
    ROOT = (Path.cwd() / "..").expanduser()
LOGO = ROOT / "pidgy.png"
DOCS = ROOT / "docs"

log = logging.getLogger("mkdocs")


def on_pre_build(config):

    if not (DOCS / LOGO.name).exists():
        log.info("move logo to docs dir")
        move(LOGO, DOCS)


def on_post_build(config):
    pass


# https://www.mkdocs.org/user-guide/configuration/#hooks
