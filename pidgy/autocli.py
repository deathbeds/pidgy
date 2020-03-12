import inspect, click, stringcase, enum, uuid, datetime, pathlib, typing, types


def autoclick(
    *object: typing.Union[types.FunctionType, click.Command], group=None, **settings
) -> click.Command:
    app = group or click.Group()
    for command in object:
        if isinstance(command, click.Command):
            app.add_command(command)
        else:
            decorators = command_from_signature(command)
            print(decorators)
            for decorator in reversed(decorators):
                command = decorator(command)
            command = app.command(
                help=inspect.getdoc(command), no_args_is_help=not decorators, **settings
            )(command)
    if len(object) == 1:
        return command
    return app


def istype(x: typing.Any, y: type) -> bool:
    if isinstance(x, type):
        return issubclass(x, y)
    return False


def click_type(
    object: typing.Union[type, tuple], default=None
) -> typing.Union[type, click.types.ParamType]:
    if isinstance(object, type):
        if issubclass(object, datetime.datetime):
            return click.DateTime()
        if issubclass(object, typing.Tuple):
            return click.Tuple(object.__args__)
        if issubclass(object, uuid.UUID):
            return click.UUID(default)
        if object is list:
            return
        if issubclass(object, typing.List):
            return click_type(object.__args__[0], default)
        if issubclass(object, set):
            return click.Choice(object)

        if issubclass(object, pathlib.Path):
            return click.Path()
        return object
    else:
        if isinstance(object, tuple):
            if all(isinstance(x, int) for x in object[:2]):
                return click.IntRange(*object)
            if all(isinstance(x, float) for x in object[:2]):
                return click.FloatRange(*object)


def command_from_signature(object: types.FunctionType, *decorators):
    for i, (k, v) in enumerate(inspect.signature(object).parameters.items()):

        if not i and k == "ctx":
            decorators += (click.pass_context,)

        if v.annotation == inspect._empty:
            continue

        if v.default == inspect._empty:
            opts = {}
            if istype(v.annotation, (typing.List, list)):
                opts.update(nargs=-1)
            decorators += (
                click.argument(
                    stringcase.spinalcase(k), type=click_type(v.annotation), **opts
                ),
            )
        else:
            type = click_type(v.annotation, v.default)
            decorators += (
                click.option(
                    "-" * (1 if len(k) == 1 else 2) + stringcase.spinalcase(k),
                    type=type,
                    show_default=True,
                    is_flag=v.annotation is bool,
                ),
            )
    return decorators
