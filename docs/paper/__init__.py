import pidgy

with pidgy.pidgyLoader():
    try:
        from . import intro
    except:
        import intro

with pidgy.pidgyLoader(main=__name__ == "__main__"):
    try:
        from . import readme
    except:
        import readme
