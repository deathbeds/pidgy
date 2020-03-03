Interactive computing as a medium for modeling ideas as computational
literature.

``pidgy`` programming
=====================



.. raw:: html

   <!--
       
       import pidgy, pathlib, nbconvert

       load = lambda x, level=1: demote(pathlib.Path(x.__file__).read_text(), level)
       demote = lambda x, i: ''.join(
           '#'*i + x if x.startswith('#') else x for x in x.splitlines(True)
       )

       def load(x, level=1):
           file = getattr(x, '__file__', x)
           name = getattr(x, '__name__', x)
           object = demote(
               pathlib.Path(file).read_text()
               if file.endswith('.md')
               else nbconvert.get_exporter('markdown')(exclude_input=True).from_filename(file)[0], level) 
           if object.startswith('---'): fm, sep, object = object.lstrip('---').partition('---')
               
           object = str.replace(object, '# ', F'# [<code>[source]</code>]({pathlib.Path(file).relative_to(pathlib.Path().absolute())})', 1)
           return object
       


       with pidgy.pidgyLoader():
           import pidgy.pytest_config.readme, pidgy.tests.test_pidgin_syntax, pidgy.tests.test_basic
           import docs, docs.best_practices

   -->




Most of those who have heard the term [Literate Programming] think of an
approach to document.




`[source] <docs/readme.md>`__\ Abstract
---------------------------------------

``pidgy`` presents a fun and expressive interactive literate programming
approach for computational literature, that is also a valid programs. A
literate program is implicitly multilingual, a document formatting
language and programming language are defined as the substrate for the
literate programming language.

The original 1979 implementation defined the [WEB] metalanguage of
[Latex] and [Pascal]. ``pidgy`` is modern and interactive take on
[Literate Programming] that uses `Markdown <#>`__ and `Python <#>`__ as
the respective document and programming languages, of course we’ll add
some other bits and bobs.

This conceptual work treats the program as literature and literature as
programs. The result of the ``pidgy`` implementation is an interactive
programming experience where authors design and program simultaneously
in `Markdown <#>`__. An effective literate programming will use machine
logic to supplement human logic to explain a program program. If the
document is a valid module (ie. it can restart and run all), the
literate programs can be imported as `Python <#>`__ modules then used as
terminal applications, web applications, formal testing object, or APIs.
All the while, the program itself is a readable work of literature as
html, pdf.

``pidgy`` is written as a literate program using `Markdown <#>`__ and
`Python <#>`__. Throughout this document we’ll discuss the applications
and methods behind the ``pidgy`` and what it takes to implement a
[Literate Programming] interface in ``IPython``.

Topics
------

-  Literate Programming
-  Computational Notebooks
-  Markdown
-  Python
-  Jupyter
-  IPython

Author
------

`Tony Fast <#>`__

.. raw:: html

   <!--

       import __init__ as paper
       import nbconvert, pathlib, click
       file = pathlib.Path(locals().get('__file__', 'readme.md')).parent / 'index.ipynb'

       @click.group()
       def application(): ...

       @application.command()
       def build():
           to = file.with_suffix('.html')
           to.write_text(
               nbconvert.get_exporter('html')(
                   exclude_input=True).from_filename(
                       str(file))[0])
           click.echo(F'Built {to}')
       import subprocess


       @application.command()
       @click.argument('files', nargs=-1)
       def push(files):
           click.echo(__import__('subprocess').check_output(
                   F"gist -u 2947b4bb582e193f5b2a7dbf8b009b62".split() + list(files)))

       if __name__ == '__main__':
           application() if '__file__' in locals() else application.callback()


   -->




`[source] <docs/best-practices.md>`__\ Best practices for literate programming
------------------------------------------------------------------------------

The first obligation of the literate programmer, defined by `Donald
Knuth <ie.%20the%20prophet%20of%20_%5BLiterate%20Programming%5D_>`__, is
a core moral commitment to write literate programs, because:

   …; surely nobody wants to admit writing an illiterate program.

      -  `Donald Knuth <#>`__ `Literate Programming <#>`__

The following best practices for literate programming have emerged while
desiging ``pidgy``.

List of best practices
~~~~~~~~~~~~~~~~~~~~~~

-  Restart and run all or it didn’t happen.

   A document should be literate in all readable, reproducible, and
   reusable contexts.

-  When in doubt, abide `Web Content Accessibility
   Guidelines <https://www.w3.org/WAI/standards-guidelines/wcag/>`__ so
   that information can be accessed by differently abled audiences.

-  `Markdown <#>`__ documents are sufficient for single units of
   thought.

   Markdown documents that translate to python can encode literate
   programs in a form that is better if version control systems that the
   ``json`` format that encodes notebooks.

-  All code should compute.

   Testing code in a narrative provides supplemental meaning to the
   ``"code"`` signifiers. They provide a test of veracity at least for
   the computational literacy.

-  ```readme.md`` <#>`__ is a good default name for a program.

   Eventually authors will compose [``"readme.md"``] documents that act
   as both the ``"__init__"`` method and ``"__main__"`` methods of the
   program.

-  Each document should stand alone, `despite all possibilities to
   fall. <http://ing.univaq.it/continenza/Corso%20di%20Disegno%20dell'Architettura%202/TESTI%20D'AUTORE/Paul-klee-Pedagogical-Sketchbook.pdf#page=6>`__
-  Use code, data, and visualization to fill the voids of natural
   language.
-  Find pleasure in writing.




[Fernando Perez], creator of [``IPython``], wrote an essay titled
`“Literate computing” and computational
reproducibility <http://blog.fperez.org/2013/04/literate-computing-and-computational.html>`__.
He defines the [Literate Computing] workflow as weaving narrative
directly into live computation. Meanwhile, [Literate Programming] refers
to complete programs that to double as literate about computational
thinking. This work explores the overlapping features of [Literate
Computing] and [Literate Programming] that allow for the co-development
of interactive computational thought to implicitly mature to readable,
reusable, and reproducible literature.

|image0|

[Literate Programming] and [Literate Computing] shine light on
perspectives on computational thinking as documentation tools for the
program and computation, respectively. From [Literate Programming], we
focus combining narrative and code to communicate human and machine
logic. [Literate Computing] considers introduces informal rich display,
derived from live computation, that can enrich as computational
narrative.

|image1|

``pidgy`` is consistent with [Literate Programming] by defining tangle
and weave steps, and it goes further to formalize testing while
interactively developing computational literature. The original 1979
``"WEB"`` implementation chose Tex and PASCAL, and this ``pidgy``
implementation chooses [Markdown] and [Python].

|image2|

Throughout this work we’ll design a purpose built interactive literate
computing interface. This work is interested in designing an interactive
experience that results in multi-objective computational documents that
are readable, reusable, and reproducible over longer timelines than
single use notebooks and programs.

.. |image0| image:: literate_computing_venn.jpeg
.. |image1| image:: tangle_weave_diagram.svg
.. |image2| image:: pidgy_literate_computing.jpeg




.. _sourcethe-pidgy-extension-for-markdownliterate-programming:

`[source] <pidgy/extension.md>`__\ The ``pidgy`` extension for `Markdown <#>`__
-------------------------------------------------------------------------------

The pidgy implementation is successful because of the existing shell
configuration system provide by the ```IPython`` <#>`__.
```IPython`` <#>`__ is an industry standard for interactive python
programming, and provided the substrate for the first
```IPython`` <#>`__ and later ```jupyter`` <#>`__ notebook
implementations. This unit specifically configurations the high-level
names we’ll refer to when extending ``pidgy`` including the tangle and
weave steps in literate computing.

.. raw:: html

   <!--excerpt-->

.. raw:: html

   <!--

       import jupyter, notebook, IPython, mistune as markdown, IPython as python, ast, jinja2 as template, importnb, doctest, pathlib
       with importnb.Notebook(lazy=True):
           try: from . import loader, tangle, extras
           except: import loader, tangle, extras
       with loader.pidgyLoader(lazy=True):
           try: from . import weave, testing, metadata
           except: import weave, testing, metadata

   -->

There are two approaches to extending the ``jupyter`` experience:

1. Write custom jupyter extensions in python and javascript. (eg.[lab
   extensions], ``IPython`` widgets)
2. Use the existing configurable objects to modify behaviors in python.
   (eg. any jupyter kernel)

``pidgy`` takes the second approach as it builds a
`Markdown <#>`__-forward REPL interface. Frequently, the
``load_ipython_extension`` method reappears frequently in this work.
This function is used by ``IPython`` to recognize modifications made by
modules to the interactive shell. The
``"load_ext reload_ext unload_ext"`` line magics used commonly by other
tools creating features for interactive computing. Demonstrated in the
following, the ``load_ipython_extension`` recieves the current
``IPython.InteractiveShell`` as an argument to be configured.

::

   def load_ipython_extension(shell: IPython.InteractiveShell) -> None:

The ``extension`` module aggregates the extensions that were designed
for ``pidgy``. Currently, ``pidgy`` defines 6 extensions to produce the
enhanced literate programming experience. Each module configures
isoluted components of the ``IPython.InteractiveShell``.

::

       [object.load_ipython_extension(shell) for object in (
           loader, tangle, extras, metadata, testing, weave
       )]
   ...

-  ``loader`` ensures the ability to important python, markdown, and
   notebook documents as reusable modules.
-  ``tangle`` defines the heuristics for translating `Markdown <#>`__ to
   [Python].
-  ``extras`` introduces experimental syntaxes specific to ``pidgy``.
-  ``metadata`` retains information as the shell and kernel interact
   with each other.
-  ``testing`` adds unittest and doctest capabilities to each cell
   execution.
-  ``weave`` defines a `Markdown <#>`__ forward display system that
   templates and displays the input.

.. raw:: html

   <!--

       def unload_ipython_extension(shell):

   `unload_ipython_extension` unloads all the extensions loads in `load_ipython_extension`.

           for x in (weave, testing, extras, metadata, tangle):
               x.unload_ipython_extension(shell)

   -->




`[source] <pidgy/events.md>`__\ The ``IPython`` step during a `Read-Eval-Print-Loop <#>`__ iteration.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   44. Sometimes I think the only universal in the computing field is
       the fetch-execute cycle. >

During a fetch-execute cycle in interactive computing, a
`Read-Eval-Print-Loop <#>`__ (ie. REPL) application transmits input to a
compiler that returns a representative display for the source.
``IPython`` is `Read-Eval-Print-Loop <#>`__ application for interactive
python programming. It is a product of the scientific computing that
required the ability interact with code to gain insight about
information.

``IPython`` is superset of [Python], it provides custom syntaxes (eg.
magics, system calls). ``IPython`` designed a configurable interface
that can customize the input source before executing a command.

.. raw:: html

   <!--

       import datetime, dataclasses, sys, IPython as python, IPython, nbconvert as export, collections, IPython as python, mistune as markdown, hashlib, functools, hashlib, jinja2.meta, ast
       exporter, shell = export.exporters.TemplateExporter(), python.get_ipython()
       modules = lambda:[x for x in sys.modules if '.' not in x and not str.startswith(x,'_')]

   -->

::

   @dataclasses.dataclass
   class Events:

The ``Events`` class is a configurable ``dataclasses`` object that
simplifies configuring code execution and metadata collection during
interactive computing sessions. There are a few note-worthy events that
``IPython`` identifies.

::

       _events = "pre_execute pre_run_cell post_execute post_run_cell".split()
       shell: IPython.InteractiveShell = dataclasses.field(default_factory=IPython.get_ipython)

       def register(self, shell=None, *, method=''):

``Events.register``\ s the object as an ``IPython`` extension, it mimics
the interface for the ``load_ipython_extension`` and
``unload_ipython_extension`` methods.

shell = shell or self.shell

::

           for event in self._events:
               callable = getattr(self, event, None)
               callable and getattr(self.shell.events, F'{method}register')(event, callable)
           if isinstance(self, ast.NodeTransformer):
               if method:

``ast.NodeTransformers`` can be used to intercept parsed [Python] code
and apply changes before compilations. If the ``Events`` object is an
``ast.NodeTransfromer`` then it is registered on the current shell.

::

                   self.shell.ast_transformers.pop(self.shell.ast_transformers.index(self))
               else:
                   self.shell.ast_transformers.append(self)

           return self

.. raw:: html

   <!--

           unregister = functools.partialmethod(register, method='un')

   -->




`[source] <pidgy/tests/test_basic.md.ipynb>`__\ A description of the pidgy metalanguage
---------------------------------------------------------------------------------------

When combined together, the pidgy extensions form the [Markdown]-forward
[Literate Programming] environment.

Everything is markdown
~~~~~~~~~~~~~~~~~~~~~~

Naming markdown blocks.
^^^^^^^^^^^^^^^^^^^^^^^

pidgy was designed so that [Python] objects can consume [Markdown].
[Markdown] content can interact with code in a few ways. \* named
variables \* doctests

Wrapping units of markdown.
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Transclusing data into the display.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Interactively testing code.
~~~~~~~~~~~~~~~~~~~~~~~~~~~


Applications
------------



`[source] <pidgy/loader.ipynb>`__\ Importing and reusing ``pidgy`` literature
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A constraint consistent across most programming languages is that
programs are executed line-by-line without any statements or
expressions. raising exceptions If literate programs have the
computational quality that they **restart and run all** the they should
When ``pidgy`` programs have this quality they can import in [Python],
they become importable essays or reports.

.. raw:: html

   <!--


       __all__ = 'pidgyLoader',
       import pidgy, sys, IPython, mistune as markdown, importnb, IPython as python
       with importnb.Notebook(lazy=True):
           try: from . import tangle, extras
           except: import tangle, extras
       if __name__ == '__main__':
           shell = get_ipython()


   -->

The ``pidgyLoader`` customizes [Python]’s ability to discover [Markdown]
and ``pidgy`` [Notebook]s have the composite ``".md.ipynb"`` extension.
``importnb`` provides a high level API for modifying how content
[Python] imports different file types.

``sys.meta_path and sys.path_hooks``

::

   class pidgyLoader(importnb.Notebook): 
       extensions = ".md .md.ipynb".split()

``get_data`` determines how a file is decoding from disk. We use it to
make an escape hatch for markdown files otherwise we are importing a
notebook.

::

   def get_data(self, path):
       if self.path.endswith('.md'):
           return self.code(self.decode())
       return super(pidgyLoader, self).get_data(path)

The ``code`` method tangles the [Markdown] to [Python] before compiling
to an [Abstract Syntax Tree].

::

   def code(self, str): 
       with importnb.Notebook(lazy=True):
           try: from . import tangle
           except: import tangle
       return ''.join(tangle.pidgy.transform_cell(str))

The ``visit`` method allows custom [Abstract Syntax Tree]
transformations to be applied.

::

       def visit(self, node):
           with importnb.Notebook():
               try: from . import tangle
               except: import tangle
           return tangle.ReturnYield().visit(node)
       

Attach these methods to the ``pidgy`` loader.

::

   pidgyLoader.code, pidgyLoader.visit = code, visit
   pidgyLoader.get_source = pidgyLoader.get_data = get_data

The ``pidgy`` ``loader`` configures how [Python] discovers modules when
they are imported. Usually the loader is used as a content manager and
in this case we hold the enter the context, but do not leave it until
``unload_ipython_extension`` is executed.

::

   def load_ipython_extension(shell):
       setattr(shell, 'loaders', getattr(shell, 'loaders', {}))
       shell.loaders[pidgyLoader] = pidgyLoader(position=-1, lazy=True)
       shell.loaders[pidgyLoader].__enter__()

.. raw:: html

   <!--

   -->




`[source] <pidgy/pytest_config/readme.md>`__\ Literature as the test
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

   import pidgy, pytest, nbval, doctest, importnb.utils.pytest_importnb

Literate documents can be motivated by the need to test a concept. In a
fact, a common use case of notebooks is that they interactively test
units of thought. Often the thought of reusability is an after thought.

``pidgy`` documents are meant to be treated as test objects. In fact,
the ``pidgy`` test suite executed by ``pytest`` through `Github
Actions <https://github.com/deathbeds/pidgy/runs/478462971>`__ uses
``pidgy`` notebooks (ie. documents with the ``".md" or ".md.ipynb"``
extension). ``pidgy`` supplies its own ``pytest`` extensions, and it
uses ```nbval`` <https://github.com/computationalmodelling/nbval/>`__
and the
``pytest``\ “–doctest-modules”\ ``flag. With these conditions we discover pytest conventions, unitests, doctests, and options cell input output validated. Ultimately,``\ pidgy\`
documents may represent units of literate that double as formal test
objects.

The document accessed by the ``"pytest11"`` console_script and includes
the extension with a pytest runner.

::

   class pidgyModule(importnb.utils.pytest_importnb.NotebookModule):

The ``pidgyModule`` derives from an existing ``pytest`` extension that
extracts formal tests from ``notebook``\ s as if they were regular
python files. We’ll use the ``pidgy.pidgyLoader`` to load
Markdown-forward documents as python objects.

::

       loader = pidgy.pidgyLoader

   class pidgyTests(importnb.utils.pytest_importnb.NotebookTests):

``pidgyTests`` makes sure to include the alternative source formats to
tangle to python executions.

::

       modules = pidgyModule,




`[source] <pidgy/readme.md>`__\ ``"readme.md"`` is a good name for a file.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   `Eat Me, Drink Me, Read
   Me. <https://medium.com/@NSomar/readme-md-history-and-components-a365aff07f10>`__

In ``pidgy``, the ``"readme.md"`` is treated as the description and
implementation of the ``__main__`` program. The code below outlines the
``pidgy`` command line application to reuse literate ``pidgy`` documents
in ``markdown`` and ``notebook`` files. It outlines how static ``pidgy``
documents may be reused outside of the interactive context.

.. raw:: html

   <!--excerpt-->

::

   ...

.. raw:: html

   <!--

       import click, IPython, pidgy, nbconvert, pathlib, re

   -->

::

   @click.group()
   def application()->None:

The ``pidgy`` ``application`` will group together a few commands that
can view, execute, and test pidgy documents.

.. raw:: html

   <!---->

``"pidgy run"`` literature as code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

   @application.command(context_settings=dict(allow_extra_args=True))
   @click.option('--verbose/--quiet', default=True)
   @click.argument('ref', type=click.STRING)
   @click.pass_context
   def run(ctx, ref, verbose):

``pidgy`` ``run`` makes it possible to execute ``pidgy`` documents as
programs, and view their pubished results.

::

       import pidgy, importnb, runpy, sys, importlib, jinja2
       comment = re.compile(r'(?s:<!--.*?-->)')
       absolute = str(pathlib.Path().absolute())
       sys.path = ['.'] + sys.path
       with pidgy.pidgyLoader(main=True), importnb.Notebook(main=True):
           click.echo(F"Running {ref}.")
           sys.argv, argv = [ref] + ctx.args, sys.argv
           try:
               if pathlib.Path(ref).exists():
                   for ext in ".py .ipynb .md".split(): ref = ref[:-len(ext)] if ref[-len(ext):] == ext else ref
               if ref in sys.modules:
                   with pidgy.pidgyLoader(): # cant reload main
                       object = importlib.reload(importlib.import_module(ref))
               else: object = importlib.import_module(ref)
               if verbose:
                   md = (nbconvert.get_exporter('markdown')(
                       exclude_output=object.__file__.endswith('.md.ipynb')).from_filename(object.__file__)[0]
                           if object.__file__.endswith('.ipynb')
                           else pathlib.Path(object.__file__).read_text())
                   md = re.sub(comment, '', md)
                   click.echo(
                       jinja2.Template(md).render(vars(object)))
           finally: sys.argv = argv

.. raw:: html

   <!---->

Test ``pidgy`` documents in pytest.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

   @application.command(context_settings=dict(allow_extra_args=True))
   @click.argument('files', nargs=-1, type=click.STRING)
   @click.pass_context
   def test(ctx, files):

Formally test markdown documents, notebooks, and python files.

::

        import pytest
        pytest.main(ctx.args+['--doctest-modules', '--disable-pytest-warnings']+list(files))

.. raw:: html

   <!---->

Install ``pidgy`` as a known kernel.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

   @application.group()
   def kernel():

``pidgy`` is mainly designed to improve the interactive experience of
creating literature in computational notebooks.

.. raw:: html

   <!---->

::

   @kernel.command()
   def install(user=False, replace=None, prefix=None):

``install`` the pidgy kernel.

::

       manager = __import__('jupyter_client').kernelspec.KernelSpecManager()
       path = str((pathlib.Path(__file__).parent / 'kernelspec').absolute())
       try:
           dest = manager.install_kernel_spec(path, 'pidgy')
       except:
           click.echo(F"System install was unsuccessful. Attempting to install the pidgy kernel to the user.")
           dest = manager.install_kernel_spec(path, 'pidgy', True)
       click.echo(F"The pidgy kernel was install in {dest}")

.. raw:: html

   <!--

       @kernel.command()
       def uninstall(user=True, replace=None, prefix=None):

   `uninstall` the kernel.

           import jupyter_client
           jupyter_client.kernelspec.KernelSpecManager().remove_kernel_spec('pidgy')
           click.echo(F"The pidgy kernel was removed.")


       @kernel.command()
       @click.option('-f')
       def start(user=True, replace=None, prefix=None, f=None):

   Launch a `pidgy` kernel applications.

           import ipykernel.kernelapp
           with pidgy.pidgyLoader():
               from . import kernel
           ipykernel.kernelapp.IPKernelApp.launch_instance(
               kernel_class=kernel.pidgyKernel)
       ...

   -->




`[source] <pidgy/kernel.md>`__\ Configuring the ``pidgy`` shell and kernel architecture.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

|image0|

Interactive programming in ``pidgy`` documents is accessed using the
polyglot [Jupyter] kernel architecture. In fact, the provenance the
[Jupyter] name is a combination the native kernel architectures for
`ju\ lia <#>`__, `pyt\ hon <#>`__, and `r <#>`__. [Jupyter]’s
generalization of the kernel/shell interface allows over 100 languages
to be used in ``notebook and jupyterlab``. It is possible to define
prescribe wrapper kernels around existing methods; this is the appraoach
that ``pidgy`` takes

   A kernel provides programming language support in Jupyter. IPython is
   the default kernel. Additional kernels include R, Julia, and many
   more.

      -  ```jupyter`` kernel
         definition <https://jupyter.readthedocs.io/en/latest/glossary.html#term-kernel>`__

``pidgy`` is not not a native kernel. It is a wrapper kernel around the
existing ``ipykernel and IPython.InteractiveShell`` configurables.
``IPython`` adds extra syntax to python that simulate literate
programming macros.

.. raw:: html

   <!--

       import jupyter_client, IPython, ipykernel.ipkernel, ipykernel.kernelapp, pidgy, traitlets, pidgy, traitlets, ipykernel.kernelspec, ipykernel.zmqshell, pathlib, traitlets

   -->

The shell is the application either jupyterlab or jupyter notebook, the
kernel determines the programming language. Below we design a just
jupyter kernel that can be installed using

-  What is the advantage of installing the kernel and how to do it.

.. code:: bash

   pidgy kernel install

Configure the ``pidgy`` shell.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

   class pidgyInteractiveShell(ipykernel.zmqshell.ZMQInteractiveShell):

Configure a native ``pidgy`` ``IPython.InteractiveShell``

::

       loaders = traitlets.Dict(allow_none=True)
       weave = traitlets.Any(allow_none=True)
       tangle = ipykernel.zmqshell.ZMQInteractiveShell.input_transformer_manager
       extras = traitlets.Any(allow_none=True)
       testing = traitlets.Any(allow_none=True)
       enable_html_pager = traitlets.Bool(True)

``pidgyInteractiveShell.enable_html_pager`` is necessary to see rich
displays in the inspector.

::

       def __init__(self,*args, **kwargs):
           super().__init__(*args, **kwargs)
           with pidgy.pidgyLoader():
               from .extension import load_ipython_extension
           load_ipython_extension(self)

Configure the ``pidgy`` kernel.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

   class pidgyKernel(ipykernel.ipkernel.IPythonKernel):
       shell_class = traitlets.Type(pidgyInteractiveShell)
       _last_parent = traitlets.Dict()

       def init_metadata(self, parent):
           self._last_parent = parent
           return super().init_metadata(parent)


       def do_inspect(self, code, cursor_pos, detail_level=0):

.. raw:: html

   <details>

Customizing the Jupyter inspector behavior for literate computing

.. raw:: html

   <p>

When we have access to the kernel class it is possible to customize a
number of interactive shell features. The do inspect function adds some
features to ``jupyter``\ ’s inspection behavior when working in
``pidgy``.

.. raw:: html

   </p>

.. raw:: html

   <pre>

::

           object = {'found': False}
           if code[:cursor_pos][-3:] == '!!!':
               object = {'found': True, 'data': {'text/markdown': self.shell.weave.format_markdown(code[:cursor_pos-3]+code[cursor_pos:])}}
           else:
               try:
                   object = super().do_inspect(code, cursor_pos, detail_level=0)
               except: ...

           if not object['found']:

Simulate finding an object and return a preview of the markdown.

::

               object['found'] = True
               line, offset = IPython.utils.tokenutil.line_at_cursor(code, cursor_pos)
               lead = code[:cursor_pos]
               col = cursor_pos - offset


               code = F"""<code>·L{
                   len(lead.splitlines()) + int(not(col))
               },C{col + 1}</code><br/>\n\n""" + code[:cursor_pos]+'·'+('' if col else '<br/>\n')+code[cursor_pos:]

               object['data'] = {'text/markdown': code}

We include the line number and cursor position to enrich the connection
between the inspector and the source code displayed on another part of
the screen.

::

           return object
       ...

.. raw:: html

   </details>

``pidgy``-like interfaces in other languages.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. |image0| image:: https://jupyter.readthedocs.io/en/latest/_images/other_kernels.png


Methods
-------



`[source] <pidgy/tangle.ipynb>`__\ Tangling [Markdown] to [Python]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``tangle`` step is the keystone of ``pidgy`` by defining the
heuristics that translate [Markdown] to [Python] execute blocks of
narrative as interactive code, and entire programs. A key constraint in
the translation is a line-for-line mapping between representations, with
this we’ll benefit from reusable tracebacks for [Markdown] source.

There are many ways to translate [Markdown] to other formats
specifically with tools like ``"pandoc"``. The formats are document
formatting language, and not programs. The [Markdown] to [Python]
translation adds a computable dimension to the document. ``pidgy`` is
one implementation and it should be possible to apply to different
heuristics to other programming languages.

.. raw:: html

   <!--
       
       import IPython, typing as τ, mistune as markdown, IPython, importnb as _import_, textwrap, ast, doctest, typing, re, dataclasses
       if __name__ == '__main__':
           import pidgy
           shell = IPython.get_ipython()

   -->

The ``pidgyTransformer`` manages the high level API the
``IPython.InteractiveShell`` interacts with for ``pidgy``. The
``IPython.core.inputtransformer2.TransformerManager`` is a configurable
class for modifying input source to before it passes to the compiler. It
is the object that introduces ``IPython``\ s line and cell magics.

::

   >>> assert isinstance(shell.input_transformer_manager, IPython.core.inputtransformer2.TransformerManager)

This configurable class has three different flavors of transformations.

-  ``shell.input_transformer_manager.cleanup_transforms``
-  ``shell.input_transformer_manager.line_transforms``
-  ``shell.input_transformer_manager.token_transformers``

   class
   pidgyTransformer(IPython.core.inputtransformer2.TransformerManager):
   def pidgy_transform(self, cell: str) -> str: return
   self.tokenizer.untokenize(self.tokenizer.parse(’’.join(cell)))

   ::

        def transform_cell(self, cell):
            return super().transform_cell(self.pidgy_transform(cell))

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.tokenizer = Tokenizer()

        def pidgy_magic(self, *text): 
            return IPython.display.Code(self.pidgy_transform(''.join(text)), language='python')

Block level lexical analysis.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Translating [Markdown] to [Python] rely only on block level objects in
the [Markdown] grammar. The ``BlockLexer`` is a modified analyzer that
adds logic to include ``doctest`` blocks in the grammar.

::

   class BlockLexer(markdown.BlockLexer):
       class grammar_class(markdown.BlockGrammar):
           doctest = doctest.DocTestParser._EXAMPLE_RE
           block_code = re.compile(r'^((?!\s+>>>\s) {4}[^\n]+\n*)+')
           default_rules = "newline hrule block_code fences heading nptable lheading block_quote list_block def_links def_footnotes table paragraph text".split()

       def parse_doctest(self, m): self.tokens.append({'type': 'paragraph', 'text': m.group(0)})

       def parse_fences(self, m):
           if m.group(2): self.tokens.append({'type': 'paragraph', 'text': m.group(0)})
           else: super().parse_fences(m)

       def parse_hrule(self, m): self.tokens.append(dict(type='hrule', text=m.group(0)))
           
       def parse_def_links(self, m):
           super().parse_def_links(m)
           self.tokens.append(dict(type='def_link', text=m.group(0)))
           
       def parse(self, text: str, default_rules=None, normalize=True) -> typing.List[dict]:
           if not self.depth: self.tokens = []
           with self: tokens = super().parse(whiten(text), default_rules)
           if normalize and not self.depth: tokens = self.normalize(text, tokens)
           return tokens
       
       depth = 0
       def __enter__(self): self.depth += 1
       def __exit__(self, *e): self.depth -= 1

The ``doctest`` token is identified before the block code.

.. raw:: html

   <!--
       
       for x in "default_rules footnote_rules list_rules".split():
           setattr(BlockLexer, x, list(getattr(BlockLexer, x)))
           getattr(BlockLexer, x).insert(getattr(BlockLexer, x).index('block_code'), 'doctest')
           if 'block_html' in getattr(BlockLexer, x):
               getattr(BlockLexer, x).pop(getattr(BlockLexer, x).index('block_html'))


   -->

Our translation creates tokens specific to each [Markdown] rule, for
code it is only necessary to identify code and paragraph tokens. The
normalizer compacts tokens into the necessary tokens.

::

   class Normalizer(BlockLexer):
       def normalize(self, text, tokens):
           """Combine non-code tokens into contiguous blocks."""
           compacted = []
           while tokens:
               token = tokens.pop(0)
               if 'text' not in token: continue
               else: 
                   if not token['text'].strip(): continue
                   block, body = token['text'].splitlines(), ""
               while block:
                   line = block.pop(0)
                   if line:
                       before, line, text = text.partition(line)
                       body += before + line
               if token['type']=='code':
                   compacted.append({'type': 'code', 'lang': None, 'text': body})
               else:
                   if compacted and compacted[-1]['type'] == 'paragraph':
                       compacted[-1]['text'] += body
                   else: compacted.append({'type': 'paragraph', 'text': body})
           if compacted and compacted[-1]['type'] == 'paragraph':
               compacted[-1]['text'] += text
           elif text.strip():
               compacted.append({'type': 'paragraph', 'text': text})
           # Deal with front matter
           if compacted[0]['text'].startswith('---\n') and '\n---' in compacted[0]['text'][4:]:
               token = compacted.pop(0)
               front_matter, sep, paragraph = token['text'][4:].partition('---')
               compacted = [{'type': 'front_matter', 'text': F"\n{front_matter}"},
                           {'type': 'paragraph', 'text': paragraph}] + compacted
           return compacted

Tokenizer logic
^^^^^^^^^^^^^^^

The tokenizer controls the translation of markdown strings to python
strings. Our major constraint is that the Markdown input should retain
line numbers.

::

   class Tokenizer(Normalizer):
       def untokenize(self, tokens: τ.List[dict], source: str = """""", last: int =0) -> str:
           INDENT = indent = base_indent(tokens) or 4
           for i, token in enumerate(tokens):
               object = token['text']
               if token and token['type'] == 'code':
                   if object.lstrip().startswith(FENCE):

                       object = ''.join(''.join(object.partition(FENCE)[::2]).rpartition(FENCE)[::2])
                       indent = INDENT + num_first_indent(object)
                       object = textwrap.indent(object, INDENT*SPACE)

                   if object.lstrip().startswith(MAGIC):  ...
                   else: indent = num_last_indent(object)
               elif token and token['type'] == 'front_matter': 
                   object = textwrap.indent(
                       F"locals().update(__import__('yaml').safe_load({quote(object)}))\n", indent*SPACE)

               elif not object: ...
               else:
                   object = textwrap.indent(object, SPACE*max(indent-num_first_indent(object), 0))
                   for next in tokens[i+1:]:
                       if next['type'] == 'code':
                           next = num_first_indent(next['text'])
                           break
                   else: next = indent       
                   Δ = max(next-indent, 0)

                   if not Δ and source.rstrip().rstrip(CONTINUATION).endswith(COLON): 
                       Δ += 4

                   spaces = num_whitespace(object)
                   "what if the spaces are ling enough"
                   object = object[:spaces] + Δ*SPACE+ object[spaces:]
                   if not source.rstrip().rstrip(CONTINUATION).endswith(QUOTES): 
                       object = quote(object)
               source += object

           # add a semicolon to the source if the last block is code.
           for token in reversed(tokens):
               if token['text'].strip():
                   if token['type'] != 'code': 
                       source = source.rstrip() + SEMI
                   break

           return source
           
   pidgy = pidgyTransformer()

.. raw:: html

   <details>

Utility functions for the tangle module

::

   def load_ipython_extension(shell):
       shell.input_transformer_manager = shell.tangle = pidgyTransformer()        

   def unload_ipython_extension(shell):
       shell.input_transformer_manager = __import__('IPython').core.inputtransformer2.TransformerManager()

   (FENCE, CONTINUATION, SEMI, COLON, MAGIC, DOCTEST), QUOTES, SPACE ='``` \\ ; : %% >>>'.split(), ('"""', "'''"), ' '
   WHITESPACE = re.compile('^\s*', re.MULTILINE)

   def num_first_indent(text):
       for str in text.splitlines():
           if str.strip(): return len(str) - len(str.lstrip())
       return 0

   def num_last_indent(text):
       for str in reversed(text.splitlines()):
           if str.strip(): return len(str) - len(str.lstrip())
       return 0

   def base_indent(tokens):
       "Look ahead for the base indent."
       for i, token in enumerate(tokens):
           if token['type'] == 'code':
               code = token['text']
               if code.lstrip().startswith(FENCE): continue
               indent = num_first_indent(code)
               break
       else: indent = 4
       return indent

   def quote(text):
       """wrap text in `QUOTES`"""
       if text.strip():
           left, right = len(text)-len(text.lstrip()), len(text.rstrip())
           quote = QUOTES[(text[right-1] in QUOTES[0]) or (QUOTES[0] in text)]
           return text[:left] + quote + text[left:right] + quote + text[right:]
       return text    

   def num_whitespace(text): return len(text) - len(text.lstrip())

   def whiten(text: str) -> str:
       """`whiten` strips empty lines because the `markdown.BlockLexer` doesn't like that."""
       return '\n'.join(x.rstrip() for x in text.splitlines())

.. raw:: html

   </details>




`[source] <pidgy/extras.ipynb>`__\ Extra langauge features of ``pidgy``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``pidgy`` experiments extra language features for python, using the same
system that IPython uses to add features like line and cell magics.

.. raw:: html

   <!--


       import IPython, typing as τ, mistune as markdown, IPython, importnb as _import_, textwrap, ast, doctest, typing, re
       import dataclasses, ast, pidgy
       with pidgy.pidgyLoader(lazy=True):
           try: from . import events
           except: import events


   -->

naming variables with gestures.
'''''''''''''''''''''''''''''''

We know naming is hard, there is no point focusing on it. ``pidgy``
allows authors to use emojis as variables in python. They add extra
color and expression to the narrative.

::

   def demojize(lines, delimiters=('_', '_')):
       str = ''.join(lines)
       import tokenize, emoji, stringcase; tokens = []
       try:
           for token in list(tokenize.tokenize(
               __import__('io').BytesIO(str.encode()).readline)):
               if token.type == tokenize.ERRORTOKEN:
                   string = emoji.demojize(token.string, delimiters=delimiters
                                          ).replace('-', '_').replace("’", "_")
                   if tokens and tokens[-1].type == tokenize.NAME: tokens[-1] = tokenize.TokenInfo(tokens[-1].type, tokens[-1].string + string, tokens[-1].start, tokens[-1].end, tokens[-1].line)
                   else: tokens.append(
                       tokenize.TokenInfo(
                           tokenize.NAME, string, token.start, token.end, token.line))
               else: tokens.append(token)
           return tokenize.untokenize(tokens).decode().splitlines(True)
       except BaseException: raise SyntaxError(str)

Top level return and yield statements.
''''''''''''''''''''''''''''''''''''''

.. raw:: html

   <!--


       def unload_ipython_extension(shell):
           shell.extras.unregister()


   -->




`[source] <pidgy/weave.md>`__\ Weaving cells in pidgin programs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. raw:: html

   <!--

       import datetime, dataclasses, sys, IPython as python, IPython, nbconvert as export, collections, IPython as python, mistune as markdown, hashlib, functools, hashlib, jinja2.meta, pidgy
       exporter, shell = export.exporters.TemplateExporter(), python.get_ipython()
       modules = lambda:[x for x in sys.modules if '.' not in x and not str.startswith(x,'_')]
       with pidgy.pidgyLoader(lazy=True):
           try:
               from . import events
           except:
               import events


   -->

pidgin programming is an incremental approach to documents.

::

   def load_ipython_extension(shell):
       shell.display_formatter.formatters['text/markdown'].for_type(str, lambda x: x)
       shell.weave = Weave(shell=shell)
       shell.weave.register()

   @dataclasses.dataclass
   class Weave(events.Events):
       shell: IPython.InteractiveShell = dataclasses.field(default_factory=IPython.get_ipython)
       environment: jinja2.Environment = dataclasses.field(default=exporter.environment)
       _null_environment = jinja2.Environment()

       def format_markdown(self, text):
           try:
               template = exporter.environment.from_string(text, globals=getattr(self.shell, 'user_ns', {}))
               text = template.render()
           except BaseException as Exception:
               self.shell.showtraceback((type(Exception), Exception, Exception.__traceback__))
           return text

       def format_metadata(self):
           parent = getattr(self.shell.kernel, '_last_parent', {})
           return {}

       def _update_filters(self):
           self.environment.filters.update({
               k: v for k, v in getattr(self.shell, 'user_ns', {}).items() if callable(v) and k not in self.environment.filters})


       def post_run_cell(self, result):
           text = strip_front_matter(result.info.raw_cell)
           lines = text.splitlines() or ['']
           IPython.display.display(IPython.display.Markdown(
               self.format_markdown(text) if lines[0].strip() else F"""<!--\n{text}\n\n-->""", metadata=self.format_metadata())
           )
           return result

   def unload_ipython_extension(shell):
       try:
           shell.weave.unregister()
       except:...

   def strip_front_matter(text):
       if text.startswith('---\n'):
           front_matter, sep, rest = text[4:].partition("\n---")
           if sep: return ''.join(rest.splitlines(True)[1:])
       return text




`[source] <pidgy/testing.md>`__\ Interactive testing of literate programs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Testing is something we added because of the application of notebooks as
test units.

A primary use case of notebooks is to test ideas. Typically this in
informally using manual validation to qualify the efficacy of narrative
and code. To ensure testable literate documents we formally test code
incrementally during interactive computing.

.. raw:: html

   <!--

       import unittest, doctest, textwrap, dataclasses, IPython, re, pidgy, sys, typing, types, contextlib, ast, inspect
       with pidgy.pidgyLoader(lazy=True):
           try: from . import events
           except: import events

   -->

::

   def make_test_suite(*objects: typing.Union[
       unittest.TestCase, types.FunctionType, str
   ], vars, name) -> unittest.TestSuite:

The interactive testing suite execute ``doctest and unittest``
conventions for a flexible interface to verifying the computational
qualities of literate programs.

::

       suite, doctest_suite = unittest.TestSuite(), doctest.DocTestSuite()
       suite.addTest(doctest_suite)
       for object in objects:
           if isinstance(object, type) and issubclass(object, unittest.TestCase):
               suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(object))
           elif isinstance(object, str):
               doctest_suite.addTest(doctest.DocTestCase(
               doctest.DocTestParser().get_doctest(object, vars, name, name, 1), doctest.ELLIPSIS))
               doctest_suite.addTest(doctest.DocTestCase(
               InlineDoctestParser().get_doctest(object, vars, name, name, 1), checker=NullOutputCheck))
           elif inspect.isfunction(object):
               suite.addTest(unittest.FunctionTestCase(object))
       return suite

   @dataclasses.dataclass
   class Testing(events.Events):

The ``Testing`` class executes the test suite each time a cell is
executed.

::

       function_pattern: str = 'test_'
       def post_run_cell(self, result):
           globs, filename = self.shell.user_ns, F"In[{self.shell.last_execution_result.execution_count}]"

           if not (result.error_before_exec or result.error_in_exec):
               with ipython_compiler(self.shell):
                   definitions = [self.shell.user_ns[x] for x in getattr(self.shell.metadata, 'definitions', [])
                       if x.startswith(self.function_pattern) or
                       (isinstance(self.shell.user_ns[x], type)
                        and issubclass(self.shell.user_ns[x], unittest.TestCase))
                   ]
                   result = self.run(make_test_suite(result.info.raw_cell, *definitions, vars=self.shell.user_ns, name=filename), result)


       def run(self, suite: unittest.TestCase, cell) -> unittest.TestResult:
           result = unittest.TestResult(); suite.run(result)
           if result.failures:
               msg = '\n'.join(msg for text, msg in result.failures)
               msg = re.sub(re.compile("<ipython-input-[0-9]+-\S+>"), F'In[{cell.execution_count}]', clean_doctest_traceback(msg))
               sys.stderr.writelines((str(result) + '\n' + msg).splitlines(True))
               return result

   @contextlib.contextmanager
   def ipython_compiler(shell):

We’ll have to replace how ``doctest`` compiles code with the ``IPython``
machinery.

::

       def compiler(input, filename, symbol, *args, **kwargs):
           nonlocal shell
           return shell.compile(
               ast.Interactive(
                   body=shell.transform_ast(
                   shell.compile.ast_parse(shell.transform_cell(textwrap.indent(input, ' '*4)))
               ).body),
               F"In[{shell.last_execution_result.execution_count}]",
               "single",
           )

       yield setattr(doctest, "compile", compiler)
       doctest.compile = compile

   def clean_doctest_traceback(str, *lines):
       str = re.sub(re.compile("""\n\s+File [\s\S]+, line [0-9]+, in runTest\s+raise[\s\S]+\([\s\S]+\)\n?"""), '\n', str)
       return re.sub(re.compile("Traceback \(most recent call last\):\n"), '', str)

.. raw:: html

   <details>

Utilities for the testing module.

::

   class NullOutputCheck(doctest.OutputChecker):
       def check_output(self, *e): return True

   class InlineDoctestParser(doctest.DocTestParser):
       _EXAMPLE_RE = re.compile(r'`(?P<indent>\s{0})'
   r'(?P<source>[^`].*?)'
   r'`')
       def _parse_example(self, m, name, lineno): return m.group('source'), None, "...", None


   def load_ipython_extension(shell):
       shell.testing = Testing(shell=shell).register()

   def unload_ipython_extension(shell):
       shell.testing.unregister()

.. raw:: html

   </details>




`[source] <pidgy/metadata.md>`__\ Capturing metadata during the interactive compute process
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To an organization, human compute time bears an important cost and
programming represents a small part of that cycle.

::

   def load_ipython_extension(shell):

The ``metadata`` module assists in collecting metadata about the
interactive compute process. It appends the metadata atrribute to the
shell.

::

       shell.metadata = Metadata(shell=shell).register()

.. raw:: html

   <!--

       import dataclasses, ast, pidgy
       with pidgy.pidgyLoader(lazy=True):
           try: from . import events
           except: import events

   -->

::

   @dataclasses.dataclass
   class Metadata(events.Events, ast.NodeTransformer):
       definitions: list = dataclasses.field(default_factory=list)
       def pre_execute(self):
           self.definitions = []

       def visit_FunctionDef(self, node):
           self.definitions.append(node.name)
           return node

       visit_ClassDef = visit_FunctionDef

.. raw:: html

   <!--

       def unload_ipython_extension(shell):
           shell.metadata.unregister()

   -->


{{load(‘readme.md’)}}

<!–


.. parsed-literal::

    [NbConvertApp] Converting notebook index.md.ipynb to rst



::

   # NBVAL_SKIP


   if __name__ == '__main__' and not '__file__' in globals():
       !jupyter nbconvert --to rst --stdout --TemplateExporter.exclude_input=True index.md.ipynb > docs/index.rst


–>
