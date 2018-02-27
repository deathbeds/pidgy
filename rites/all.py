def load_ipython_extension(ip):
    from . import markdown, template, testing
    [module.load_ipython_extension(ip)for module in (markdown, testing, template)]