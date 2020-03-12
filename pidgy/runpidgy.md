# Scripting with literate programs.

`pidgy` is based on [Python], a scripting language, therefore it should be possible execute markdown as scripts.

    def run(object: str, run_name=None, **globals):

`run` executes a literate document as a script.

        import pidgy, importnb, sys, importlib, pathlib, runpy
        _root_in_sys = '.' not in sys.path
        if not _root_in_sys:
            sys.path = ['.'] + sys.path
        try:
            with pidgy.pidgyLoader(), importnb.Notebook():

It appears the loaders only work with `runpy.run_module`, not `runpy.run_path`.

                return runpy.run_module(prepare_name(object), globals, '__main__')

        finally:
            if not _root_in_sys:
                sys.path.pop(sys.path.index('.'))
    def render(ref: str):
        import pathlib, pidgy, re
        object = run(ref)
        if object['__file__'].endswith(('.py', '.md', '.markdown')):
            body = pathlib.Path(object['__file__']).read_text()
            return pidgy.weave.exporter.environment.from_string(
                re.sub('(<!--[\s\S]*-->?)', '', body)
            ).render(object).rstrip() + '\n'

    def prepare_name(str):
        parts = list(__import__('pathlib').Path(str).parts)
        for ext in ".py .ipynb .md".split():
            parts[-1] = parts[-1][:-len(ext)] if parts[-1][-len(ext):] == ext else parts[-1]
        return '.'.join(parts)


    def alias_to_module_name(object: str) -> str:

Convert a filename to a module specification.

        path = pathlib.Path(object)
        if path.exists():
            parts = list(path.parts)
        for ext in ".py .ipynb .md".split():
            parts[-1] = parts[-1][:-len(ext)] if parts[-1][-len(ext):] == ext else parts[-1]
        object = '.'.join(parts)
        return object
