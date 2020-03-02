from .. import loader


def pytest_collect_file(parent, path):
    with loader.pidgyLoader(lazy=True):
        from . import readme
    return readme.pidgyTests(parent, path)
