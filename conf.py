def setup(app):
    def on_config_inited(app, error):
        try:
            __import__("jupyterlite")
        except (ImportError, AttributeError):
            print("jupyterlite not available, no big")
            return

        from subprocess import check_call

        wheel = ["pip", "wheel", "--w=dist", "--no-deps"]
        check_call([*wheel, "."])
        check_call([*wheel, "htmlmin"])
        check_call(["jupyter", "lite", "build"], cwd="lite")

    app.connect("config-inited", on_config_inited)


author = "deathbeds"
comments_config = {"hypothesis": False, "utterances": False}
copyright = "2021"
exclude_patterns = [
    "_build",
    ".DS_Store",
    ".nox",
    ".pytest_cache",
    "**.ipynb_checkpoints",
    "jupyter_execute",
    "Thumbs.db",
]
execution_allow_errors = False
execution_excludepatterns = []
execution_in_temp = False
execution_timeout = 30
extensions = [
    "sphinx_togglebutton",
    "sphinx_copybutton",
    "myst_nb",
    "jupyter_book",
    "sphinx_thebe",
    "sphinx_comments",
    "sphinx_external_toc",
    "sphinx.ext.intersphinx",
    "sphinx_panels",
    "sphinx_book_theme",
    "sphinx_jupyterbook_latex",
]
external_toc_exclude_missing = False
external_toc_path = "_toc.yml"
html_baseurl = ""
html_favicon = ""
html_logo = "pidgy.png"
html_sourcelink_suffix = ""
html_static_path = ["lite/_output"]
html_theme = "sphinx_book_theme"
html_theme_options = {
    "search_bar_text": "Search this book...",
    "launch_buttons": {
        "notebook_interface": "classic",
        "binderhub_url": "https://mybinder.org",
        "jupyterhub_url": "",
        "thebe": False,
        "colab_url": "",
    },
    "path_to_docs": "",
    "repository_url": "https://github.com/executablebooks/jupyter-book",
    "repository_branch": "master",
    "google_analytics_id": "",
    "extra_navbar": 'Powered by <a href="https://jupyterbook.org">Jupyter Book</a>',
    "extra_footer": "",
    "home_page_in_toc": True,
    "use_repository_button": False,
    "use_edit_page_button": False,
    "use_issues_button": False,
}
html_title = "Pidgy Programming"
jupyter_cache = ""
jupyter_execute_notebooks = "off"
language = None
latex_engine = "pdflatex"
latex_logo = "pidgy.png"
myst_enable_extensions = [
    "colon_fence",
    "dollarmath",
    "linkify",
    "substitution",
    "tasklist",
]
myst_url_schemes = ["mailto", "http", "https"]
nb_output_stderr = "show"
numfig = True
panels_add_bootstrap_css = False
pygments_style = "sphinx"
suppress_warnings = ["myst.domains"]
use_jupyterbook_latex = True
use_multitoc_numbering = True
