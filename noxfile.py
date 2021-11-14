from nox import session
from nox.sessions import _SessionQuit
from os import getenv

CI = bool(getenv("CI"))


@session(reuse_venv=True)
def docs(session):
    session.install("jupyter-book", "sphinx-autoapi", "-e.")
    session.run("python", "-m", "pidgy.kernel.install")
    session.run("jb", "build", ".")


@session(reuse_venv=not CI, python=False)
def test(session):
    session.install(CI and ".[test]" or "-e.[test]")
    session.run("python", "-m", "pidgy.kernel.install")
    session.run("pytest", "--nbval", *session.posargs)


@session(reuse_venv=True)
def lint(session):
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files")
