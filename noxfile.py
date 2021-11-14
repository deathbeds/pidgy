from nox import session
from nox.sessions import _SessionQuit
from os import getenv

CI = bool(getenv("CI"))


@session(reuse_venv=True)
def docs(session):
    session.install("jupyter-book", "sphinx-autoapi", "-e.")
    session.run("jb", "build", ".")


@session(reuse_venv=not CI)
def test(session):
    session.install(CI and ".[test,kernel]" or "-e.[test,kernel]")
    session.run("python", "-m", "pidgy.kernel.install")
    session.run("jupyter", "kernelspec", "list")
    session.run("pytest", "--nbval", *session.posargs)


@session(reuse_venv=True)
def lint(session):
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files")
