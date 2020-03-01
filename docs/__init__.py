import pidgy

with pidgy.pidgyLoader(lazy=True):
    try:
        from . import intro, best_practices
    except:
        import intro, best_practices
