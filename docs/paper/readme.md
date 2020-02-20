# `pidgy` programming

## Abstract

`pidgy` is a literate program that specifies and implements a literate
programming language using [Markdown] as the document formatting language and
[Python] as the programming language. The implementation extends the interactive
python shell that commonly powers `jupyter` notebooks. Through this program we
will learn how `pidgy` tangles markdown to python code, incrementally runs
formal tests on your input, and presents woven markdown output that allows for
transclusion of variables.

## Topics

- Literate Programming
- Computational Notebooks
- Markdown
- Python
- Jupyter
- IPython

## Author

[Tony Fast]

<!--

    import __init__ as paper
    import nbconvert, pathlib, click
    file = pathlib.Path(locals().get('__file__', 'readme.md')).parent / 'index.ipynb'


    @click.command()
    def build():
        file.with_suffix('.md').write_text(
            nbconvert.get_exporter('markdown')(
                exclude_input=True).from_filename(
                    str(file))[0])
        click.echo(F'Built {file.with_suffix(".md")}')

    if __name__ == '__main__':
         build() if '__file__' in locals() else build.callback()


-->

[tony fast]: #
[markdown]: #
[python]: #
[jupyter]: #
[ipython]: #
