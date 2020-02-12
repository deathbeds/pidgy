from .. import reuse
def pytest_collect_file(parent, path):
    with reuse.pidgyLoader(lazy=True):
        from . import readme
    return readme.pidgyTests(parent, path)