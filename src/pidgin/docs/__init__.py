import pidgin

with pidgin.Pidgin(lazy=True):
    from . import readme, testing_notebooks