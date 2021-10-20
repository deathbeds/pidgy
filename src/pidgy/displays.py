"""weave the literate code in rich displays

weaving in literate programming refers to the
representation of the document language as a form.
this module provides the machinery necessary to weave
`pidgy` input into fun, interactive experiences."""

import collections
import contextlib
import functools
import io
import sys
import warnings

import IPython
import jinja2.meta
import traitlets

from . import get_ipython

ENVS = {}


class Undefined(jinja2.Undefined):
    """handle undefined templates in jinja2"""

    def _fail_with_undefined_error(self, *args, **kwargs):
        # log that the template failed
        return ""


def is_first_line_blank(s):
    """determine if the first line of string is empty"""
    return not bool(io.StringIO(s).readline().strip())


def get_environment(async_=False):
    """retrieve singleton jinja2 environment."""
    # we maintain sync and async environments separately
    global ENVS
    if async_ in ENVS:
        return ENVS[async_]

    ENVS[async_] = ENVIRONMENT = jinja2.Environment(
        enable_async=async_,
        loader=jinja2.ChoiceLoader(
            [jinja2.FileSystemLoader("."), jinja2.DictLoader({})]
        ),
        cache_size=0,
        undefined=Undefined,
        finalize=Finalize(),
    )

    return ENVIRONMENT


class Env(traitlets.HasTraits):
    """a traitlets with a jinja environment"""

    environment = traitlets.Any()
    modules = traitlets.List(["__main__", "builtins"])

    @traitlets.default("environment")
    def denvironment(self):
        return get_environment()

    def ns(self):
        return collections.ChainMap(
            *(vars(__import__(x)) for x in self.modules),
            get_ipython().user_ns.get("__annotations__", {}),
        )


class Value(traitlets.HasTraits):
    """a non widget widget that has an observable value"""

    value = traitlets.Any()

    @traitlets.observe("value")
    def update(self, *args):
        if self.display_handle:
            self.display_handle.update(
                IPython.display.Markdown(self.value)
                if isinstance(self.value, str)
                else self.value
            )

    display_handle = traitlets.Any()
    display_cls = traitlets.Any(IPython.display.Markdown)

    def _ipython_display_(self):
        if self.display_handle is None:
            import IPython

            self.display_handle = IPython.display.DisplayHandle()

        self.display_handle.display(
            IPython.display.Markdown(self.value)
            if isinstance(self.value, str)
            else self.value
        )


class Template(Env, Value):
    """a sync/async template that can display and update itself"""

    template = traitlets.Any()
    vars = traitlets.Set()

    iframe_width = traitlets.Any("100%")
    iframe_height = traitlets.Any(600)

    def update(self, *args):
        if self.display_handle:
            if self.vars:
                import asyncio

                asyncio.ensure_future(self.aupdate())
            else:
                self.display_handle.update(self.get_display())

    def render(self):
        self.value = self.template.render(**self.ns())
        return self.value

    def get_display(self):
        try:
            object = self.render()
        except RuntimeError:
            from nest_asyncio import apply

            apply()
            return self.get_display()
        if object.startswith(("http://", "https://")):
            return IPython.display.IFrame(object, self.iframe_width, self.iframe_height)
        return IPython.display.Markdown(object)

    def _ipython_display_(self):
        import IPython

        if self.display_handle is None:

            self.display_handle = IPython.display.DisplayHandle()

        self.display_handle.display(self.get_display())


def observe(self, id, x):
    self.displays[id].update()


class IDisplays(Env):
    widgets = traitlets.Dict()
    tests = traitlets.Dict()
    displays = traitlets.Dict()
    state = traitlets.Dict()

    def loader(self):
        import jinja2

        for loader in self.environment.loader.loaders:
            if isinstance(loader, jinja2.DictLoader):
                return loader

    def display(self, object):
        import jinja2.meta

        vars = jinja2.meta.find_undeclared_variables(self.environment.parse(object))

        import emoji

        object = emoji.emojize(object, use_aliases=True)

        template = Template(
            template=self.environment.from_string(object),
            vars=vars,
            id=id,
        )
        IPython.display.display(template)

    def vars(self):
        return set(
            x for v in get_ipython().displays_manager.displays.values() for x in v.vars
        )

    def get_state(self, *vars):
        ns = self.ns()
        return {x: ns.get(x) for x in vars or self.vars()}


def get_active_types(shell=None):
    """get the active types in the current IPython shell.
    we ignore latex, but i forget why."""
    import IPython

    shell = shell or IPython.get_ipython()
    if shell:
        object = list(shell.display_formatter.active_types)
        object.insert(object.index("text/html"), object.pop(object.index("text/latex")))
        return reversed(object)
    return []


def get_minified(x):
    """minify html"""
    return __import__("htmlmin").minify(x, False, True, True, True, True, True, True)


def get_decoded(object):

    if isinstance(object, bytes):
        object = __import__("base64").b64encode(object).decode("utf-8")
    return object


class Finalize:
    """a callable trait that uses the current ipython display formatter to update jinja2 templates."""

    def normalize(self, type, object, metadata) -> str:
        """normalize and object with (mime)type and return a string."""
        if type == "text/html" or "svg" in type:
            object = get_minified(object)

        if type.startswith("image"):
            width, height = (
                metadata.get(type, {}).get("width"),
                metadata.get(type, {}).get("height"),
            )
            object = get_decoded(object)
            object = (
                f"""<img src="data:image/{type.partition('/')[2]};base64,{object}"/>"""
            )
        return object

    def __call__(self, object):
        """try to convert the object into a markdown or html
        representation using the current ipython shell."""
        datum = get_ipython().display_formatter.format(object)
        data, metadata = datum if isinstance(datum, tuple) else (datum, {})
        try:
            key = next(filter(data.__contains__, get_active_types(get_ipython())))
        except StopIteration:
            return str(object)
        if key == "text/plain":
            return str(object)
        return self.normalize(key, data[key], metadata)


def post_run_cell(result):
    if not (result.error_before_exec or result.error_in_exec):
        self = get_ipython().displays_manager

        if not is_first_line_blank(result.info.raw_cell):
            self.display(result.info.raw_cell)


def load_ipython_extension(shell):
    shell.add_traits(displays_manager=traitlets.Any())
    shell.displays_manager = IDisplays()
    shell.events.register(post_run_cell.__name__, post_run_cell)


def unload_ipython_extension(shell):

    shell.events.unregister(post_run_cell.__name__, post_run_cell)


def is_widget(object):
    """is an object a widget"""
    if "ipywidgets" in sys.modules:
        if isinstance(object, __import__("ipywidgets").Widget):
            return True
    return False


def was_displayed(object):
    # the best we can know is if the widget was ever displayed
    return object._trait_values.get("_display_callbacks") is not None
