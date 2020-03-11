# Literate scripting

`pidgy` is based on [Python], a scripting language, therefore it should be possible execute markdown as scripts.

    def prepare_name(str):
        parts = list(__import__('pathlib').Path(str).parts)
        for ext in ".py .ipynb .md".split():
            parts[-1] = parts[-1][:-len(ext)] if parts[-1][-len(ext):] == ext else parts[-1]
        return '.'.join(parts)


    def run(object: str, run_name=None, **globals):

`run` executes a literate document as a script.

        import pidgy, importnb, sys, importlib, pathlib, runpy
        _root_in_sys = '.' not in sys.path
        if not _root_in_sys:
            sys.path = ['.'] + sys.path
        try:
            with pidgy.pidgyLoader(), importnb.Notebook():

It appears the loaders only work with `runpy.run_module`, not `runpy.run_path`.

                return runpy.run_module(prepare_name(object), globals, run_name)

        finally:
            if not _root_in_sys:
                sys.path.pop(sys.path.index('.'))

    def alias_to_module_name(object: str) -> str:

Convert a filename to a module specification.

        path = pathlib.Path(object)
        if path.exists():
            parts = list(path.parts)
        for ext in ".py .ipynb .md".split():
            parts[-1] = parts[-1][:-len(ext)] if parts[-1][-len(ext):] == ext else parts[-1]
        object = '.'.join(parts)
        return object
