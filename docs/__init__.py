import pidgy

with pidgy.pidgyLoader(lazy=True):
    try:
        from . import intro, best_practices
    except:
        import intro, best_practices
main = __name__ == "__main__"
with pidgy.pidgyLoader(main=main, lazy=not main):
    try:
        from . import readme
    except:
        import readme
