from . import conventions, markdown, template, testing

def load_ipython_extension(ip):
    for module in (conventions, markdown, testing, template):
        if module.__complete__ is not True:
            raise module.__complete__
        module.load_ipython_extension(ip)