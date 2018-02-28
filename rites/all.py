from . import conventions, markdown, template, testing
from IPython import get_ipython
def load_ipython_extension(ip=get_ipython()):
    for module in (markdown, testing, template, conventions):
        if module.__complete__ is not True:
            raise module.__complete__
        module.load_ipython_extension(ip)