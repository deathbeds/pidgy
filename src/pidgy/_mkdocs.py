def define_env(env):
    pass


def on_pre_page_macros(env):
    from io import StringIO
    from runpy import _run_module_code

    from ..run import Markdown

    env.page.shebang = None
    if env.page.markdown.startswith("#!/usr/bin/env"):
        buffer = StringIO(env.page.markdown)
        env.page.shebang = next(buffer)
        env.page.markdown = "".join(buffer)
        env.variables.update(Markdown().load_code(env.page.markdown, env.page.file.src_path))
