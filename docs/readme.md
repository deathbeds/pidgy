# Abstract

`pidgy` presents a fun and expressive interactive literate programming approach
for computational literature, that is also a valid programs.
A literate program is implicitly multilingual, a document formatting language
and programming language are defined as the substrate for the
literate programming language.

The original 1979 implementation defined the [WEB] metalanguage
of [Latex] and [Pascal]. `pidgy` is modern and interactive
take on [Literate Programming] that uses [Markdown] and [Python]
as the respective document and programming languages,
of course we'll add some other bits and bobs.

This conceptual work treats the program as literature and literature
as programs. The result of the `pidgy` implementation is an interactive programming
experience where authors design and program simultaneously in [Markdown].
An effective literate programming will use machine logic to supplement
human logic to explain a program program.
If the document is a valid module (ie. it can restart and run all),
the literate programs can be imported as [Python] modules
then used as terminal applications, web applications,
formal testing object, or APIs. All the while, the program
itself is a readable work of literature as html, pdf.

`pidgy` is written as a literate program using [Markdown]
and [Python].
Throughout this document we'll discuss
the applications and methods behind the `pidgy`
and what it takes to implement a [Literate Programming]
interface in `IPython`.

# Topics

- Literate Programming
- Computational Notebooks
- Markdown
- Python
- Jupyter
- IPython

# Author

[Tony Fast]

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

[tony fast]: #
[markdown]: #
[python]: #
[jupyter]: #
[ipython]: #
