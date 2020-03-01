import pidgy

with pidgy.pidgyLoader(lazy=True):
    try:
        from . import intro
    except:
        import intro
