collect_ignore = ["site"]

def pytest_collectstart(collector):
    if collector.fspath and collector.fspath.ext == '.ipynb':
        collector.skip_compare += 'text/plain',




def pytest_load_initial_conftests(args):
    from shlex import split
    args[:] =  split(
        "-pno:warnings -p no:importnb --ignore lite --cov pidgy --cov-report term --cov-report html --nbval-current-env --nbval --nbval-sanitize-with sanitize.cfg"
    ) + args