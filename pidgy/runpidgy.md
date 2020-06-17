# Scripting with literate programs.

Since `pidgy` is based on [Python], derived pidgy documents can be used as scripts.

A `pidgy` program executed as the **main** program has similar state to the running notebook and it introduces the file object.

`pidgy` is based on [Python], a scripting language, therefore it should be possible execute markdown as scripts.

    import types, pidgy, ast, runpy, importlib, sys
    __all__ = 'run', 'render', 'Runner'


    def run(object: str, **globals) -> dict:

`run` executes a literate document as a script.

        return Runner(object).run(**globals)

    def render(object: str, **globals) -> dict:

`render` executes a templated document.

        return Runner(object).render(**globals)

    ...

    class Runner(pidgy.pidgyLoader):

A script `Runner` for `pidgy` documents based off the `importnb` machinery.

        def __init__(self, name, path=None, *args, **kwargs):
            if path is None: path = name
            super().__init__(name, path, *args, **kwargs)
        def visit(self, node):
            node = super().visit(node)
            if sys.version_info[1] > 7:
                body, annotations = ast.Module([], []), ast.Module([], [])
            else:
                body, annotations = ast.Module([]), ast.Module([])
            while node.body:
                element = node.body.pop(0)
                if isinstance(element, ast.AnnAssign) and element.target.id[0].islower():
                    try:
                        if element.value:
                            ast.literal_eval(element.value)
                        annotations.body.append(element)
                        continue
                    except: ...
                if isinstance(element, (ast.Import, ast.ImportFrom)):
                    annotations.body.append(element)
                body.body.append(element)
            self.arg_code = compile(annotations, self.path, 'exec')
            return body

        def create_module(loader, spec=None):

When the module is created. Compile the source to code to discover arguments in the code.

            if spec is None:
                spec = importlib.util.spec_from_loader(loader.name, loader)
                module = super().create_module(spec)
            loader.main_code = loader.get_code(loader.name)
            runpy._run_code(loader.arg_code, vars(module), {}, '__main__', spec, None, None)
            return module

        def exec_module(loader, module=None, **globals):
            module = module or loader.create_module()
            vars(module).update(globals)
            runpy._run_code(loader.main_code, vars(module), {}, '__main__', module.__spec__, None, None)
            return module

        def run(loader, **globals):
            return loader.exec_module(**globals)

        def render(loader, **globals):
            return loader.format(loader.run(**globals))

        def cli(loader):
            import pidgy.compat.autoclick, click
            module = loader.create_module()
            def main(verbose: bool=True, **globals):
                nonlocal module
                try:
                    loader.exec_module(module, **globals)
                    verbose and click.echo(pidgy.util.ansify(loader.format(module)))
                except SystemExit: ...

            pidgy.compat.autoclick.command_from_decorators(main,
                                                  click.option('--verbose/--silent', default=True),
                                                  *pidgy.compat.autoclick.decorators_from_module(module)).main()

        def format(loader, module):
            import nbconvert, operator, builtins
            if loader.path.endswith(('.py', '.md', '.markdown')):
                return nbconvert.TemplateExporter().environment.from_string(
                    pidgy.util.strip_front_matter(
                        pidgy.util.strip_html_comment(
                            pidgy.util.strip_shebang(
                                loader.decode())))
                ).render({
                    **vars(operator), **vars(builtins),
                    **vars(module)}).rstrip() + '\n'

    ...

## shebang statements in literate programs.

A feature of `pidgy` markdown files, not notebook files, is that a shebang statement can be included at the beginning to indicate how a document is executed.

Some useful shebang lines to being pidgy documents with.

    #!/usr/bin/env pidgy run
    #!/usr/bin/env python -m pidgy run
    #!/usr/bin/env python -m pidgy render
    #!/usr/bin/env pidgy render
