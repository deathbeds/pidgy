from os import getenv

from nox import session, parametrize, options

options.sessions = ["docs(html)", "test"]

CI = bool(getenv("CI"))


@session(venv_backend="conda", reuse_venv=True, python="3.9")
@parametrize("pdf", [False, True], ids=["html", "pdf"])
def docs(session, pdf):
    "build the `pidgy` documentation with `jupyter-book`"
    if pdf:
        session.posargs += "-builder", "pdflatex"
        session.conda_install("-c", "conda-forge", "tectonic")
    session.install("jupyter-book", "jupyterbook-latex", "sphinx-autoapi", "-e.")

    session.run("jb", "build", ".", *session.posargs)


@session(reuse_venv=not CI)
def test(session):
    "test the `pidgy` project with `pytest`"
    session.install(CI and ".[test,kernel]" or "-e.[test,kernel]")
    session.run("python", "-m", "pidgy.kernel.install")
    session.run("jupyter", "kernelspec", "list")
    session.run("pytest", "--nbval", *session.posargs)


@session(reuse_venv=True)
def lint(session):
    "test the `pidgy` project with `black and isort` w `pre-commit`"
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files", *session.posargs)
