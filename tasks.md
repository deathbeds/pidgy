# developer tasks for pidgy

> these tasks are imported in `dodo.py`. these tasks are executed with the `doit` cli, type `doit list` to get started.

## tasks

these tasks will help us maintain project level api's that work for local and remote development
    
### `doit` task configuration

    DOIT_CONFIG = dict(
        verbosity=2
    )
    
### formatting

    def task_format():

format the content the way `pidgy` prefers it,

        return dict(
            actions="""
    isort .
    black .
    isort .
            """.strip().splitlines()
        )


### documentation

#### documentation configuration

    def task_conf_py():

format the `conf.py` for sphinx from `jupyter-book`

        return dict(
            file_dep="docs/toc.yml docs/config.yml".split(), actions=[
                "jb config sphinx --toc docs/toc.yml --config docs/config.yml . > conf.py"
            ], targets=["conf.py"]
        )

#### documentation build

    def task_docs():

build the docs with `sphinx`s builders

        return dict(
            file_dep=["conf.py"], actions=[
                "sphinx-build . _build/html"
            ], targets=["_build/html/index.html"]
        )

### testing