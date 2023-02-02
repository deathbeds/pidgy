"""pidgy weaves commonmark markdown into rich, reactive displays."""

from re import compile
from typing import ChainMap

from IPython import get_ipython
from jinja2 import Environment, Template, Undefined
from traitlets import Instance

CELL_MAGIC = compile("^\s*%{2}\S")
NO_SHOW = compile(r"^\s*\r?\n")

from IPython import get_ipython

URL = compile("^(http[s]|file)://")


class Finalizer:
    def __new__(cls, object):
        return object


class IPythonFinalizer(Finalizer):
    """a finalizer that extracts content from IPython displays"""

    @staticmethod
    def normalize(type, object, metadata) -> str:
        """normalize and object with (mime)type and return a string."""

        if type == "text/html" or "svg" in type:
            object = get_minified(object)

        if type.startswith("image"):
            md = metadata.get(type, {})
            width, height = md.get("width"), md.get("height")
            object = get_decoded(object)
            *_, data = type.partition("/")
            object = f"""<img src="data:image/{data};base64,{object}"/>"""

        return object

    def __new__(cls, object):
        """convert an object into a markdown/html representation"""

        shell = get_ipython()
        datum = shell.display_formatter.format(object)
        data, metadata = datum if isinstance(datum, tuple) else (datum, {})
        key = next(filter(data.__contains__, get_active_types(shell)), str(object))
        if key == "text/plain":
            return str(object)
        return cls.normalize(key, data[key], metadata)


class IPythonEnvironment(Environment):
    def init_filters(self):
        from . import filters

        self.filters.update(
            (k, v) for k, v in vars(filters).items() if k[0].isalpha() and callable(v)
        )

    def __init__(self, *args, **kwargs):
        from jinja2 import ChoiceLoader, DictLoader, FileSystemLoader

        kwargs.setdefault("loader", ChoiceLoader([DictLoader({}), FileSystemLoader(".")]))
        kwargs.setdefault("finalize", IPythonFinalizer)
        kwargs.setdefault("undefined", Undefined)
        kwargs.setdefault("enable_async", True)
        super().__init__(*args, **kwargs)
        self.init_filters()


class IPythonTemplate(Template):
    def ns(self, *args, **kwargs):
        import builtins

        ns = get_ipython()
        if ns:
            return ChainMap(kwargs, ns.user_ns, vars(builtins))
        return {}

    def render(self, *args, **kwargs):
        try:
            return super().render(self.ns(*args, **kwargs))
        except RuntimeError:
            import nest_asyncio

            nest_asyncio.apply()
            return super().render(self.ns(*args, **kwargs))

    async def render_async(self, *args, **kwargs):
        return await super().render_async(self.ns(*args, **kwargs))

    async def generate_async(self, *args, **kwargs):
        async for x in super().generate_async(self.ns(*args, **kwargs)):
            yield x


class Undefined(Undefined):
    def __str__(self, *args, **kwargs):
        # log that the template failed
        if self._undefined_obj:
            return f"`{self._undefined_name} of {self._undefined_obj} is undefined`"
        return f"`{self._undefined_name} is undefined`"


def get_active_types(shell=None):
    """get the active types in the current IPython shell.
    we ignore latex, but i forget why."""
    shell = shell or get_ipython()
    if shell:
        object = list(shell.display_formatter.active_types)
        object.insert(object.index("text/html"), object.pop(object.index("text/latex")))
        return reversed(object)
    return []


def get_minified(x):
    return x


def get_decoded(object):
    if isinstance(object, bytes):
        from base64 import b64encode

        object = b64encode(object).decode("utf-8")
    return object


def get_environment(reuse=True, _cache={}, **kwargs):
    # use this function to avoid repeat environment instantiation
    shell = get_ipython()
    if shell:
        try:
            return shell.environment
        except AttributeError:
            pass
    if reuse:
        if _cache:
            return _cache[True]
        _cache[True] = IPythonEnvironment(**kwargs)
        return _cache[True]
    return IPythonEnvironment(**kwargs)


def load_ipython_extension(shell):
    if not shell.has_trait("environment"):
        shell.add_traits(environment=Instance(IPythonEnvironment, default_value=get_environment()))


def unload_ipython_extension(shell):
    pass
