"jinja2 filters that make writing pidgy more fun"


def q(q, cite):
    """a filter for <q>uotes"""
    return f"""<q cite="{cite}">{q}</q>"""
