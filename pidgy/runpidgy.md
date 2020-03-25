# Scripting with literate programs.

Since `pidgy` is based on [Python], derived pidgy documents can be used as scripts.

A `pidgy` program executed as the **main** program has similar state to the running notebook and it introduces the file object.

`pidgy` is based on [Python], a scripting language, therefore it should be possible execute markdown as scripts.

    import types, pidgy, ast
    def run(object: str, run_name=None, **globals) -> dict:

`run` executes a literate document as a script.

        import pidgy, importnb, sys, importlib, pathlib, runpy
        loader = pidgy.pidgyLoader(object, object)
        spec = importlib.util.spec_from_loader(loader.name, loader)

        main_code = loader.get_code(loader.name)
        module = types.ModuleType(loader.name)
        return runpy._run_code(main_code, vars(module), globals, '__main__', spec, None, None)

    def render(ref: str, **globals): return format_output(parameterize(ref, **globals))

    def format_output(object):
        import pathlib, pidgy, re, operator, builtins, nbconvert
        if object['__file__'].endswith(('.py', '.md', '.markdown')):
            body = pathlib.Path(object['__file__']).read_text()
            return nbconvert.TemplateExporter().environment.from_string(
                pidgy.util.strip_front_matter(
                    pidgy.util.strip_html_comment(
                        pidgy.util.strip_shebang(
                            body)))
            ).render({
                **vars(operator), **vars(builtins),
                **object}).rstrip() + '\n'
    ...

## Parameterizing a script

Reward good behavior for using type annotations. Type annotations are important for other applications using your technology.

    def parameterize(file, **globals):

Run a script with annotated variables as arguements.

        import ast, pytest, builtins, types, runpy, importlib, inspect, pytest, sys, click
        loader = CLILoader(file, file)
        spec = importlib.util.spec_from_loader(loader.name, loader)

        main_code, arg_code = loader.get_code(loader.name), compile(loader.annotations, loader.path, 'exec')

        module = types.ModuleType(loader.name)
        annotations = runpy._run_code(arg_code, vars(module), {}, '__main__', spec, None, None)
        vars(module).update(annotations)
        decorators = pidgy.autocli.decorators_from_dict(annotations)

        @click.pass_context
        def cli(ctx, **kwargs):
            nonlocal module, globals
            vars(module).update(kwargs, ctx=ctx)
            vars(module).update(globals)
            runpy._run_code(main_code, vars(module), {}, '__main__', spec, None, None)

        command = pidgy.autocli.command_from_decorators(cli, *decorators)
        try:
            command.main()
        except SystemExit: ...
        return vars(module)

    class CLILoader(pidgy.pidgyLoader):
        def visit(self, node):
            node = super().visit(node)
            self.body, self.annotations = ast.Module([]), ast.Module([])
            while node.body:
                element = node.body.pop(0)
                if isinstance(element, ast.AnnAssign) and element.target.id[0].islower():
                    try:
                        if element.value:
                            ast.literal_eval(element.value)
                        self.annotations.body.append(element)
                        continue
                    except: ...
                if isinstance(element, (ast.Import, ast.ImportFrom)):
                    self.annotations.body.append(element)
                self.body.body.append(element)
            return self.body

## shebang statements in literate programs.

A feature of `pidgy` markdown files, not notebook files, is that a shebang statement can be included at the beginning to indicate how a document is executed.

Some useful shebang lines to being pidgy documents with.

    #!/usr/bin/env pidgy run
    #!/usr/bin/env python -m pidgy run
    #!/usr/bin/env python -m pidgy render
    #!/usr/bin/env pidgy render
