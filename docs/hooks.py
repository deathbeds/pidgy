from pathlib import Path
import logging
from shutil import move

HERE = Path.cwd()
LOGO = HERE / "pidgy.png"
DOCS = HERE / "docs"

log = logging.getLogger('mkdocs')

def on_pre_build(config):
    
    if not (DOCS / LOGO.name).exists():
        log.info("move logo to docs dir")
        move(LOGO, DOCS)

def on_post_build(config):
    pass
    
# https://www.mkdocs.org/user-guide/configuration/#hooks