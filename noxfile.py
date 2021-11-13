from nox import session
from nox.sessions import _SessionQuit


@session(reuse_venv=True)
def docs(session):
    session.install("jupyter-book", "sphinx-autoapi", "-e.")
    session.run("jb", "build", ".")


@session(reuse_venv=True)
def lint(session):
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files")
