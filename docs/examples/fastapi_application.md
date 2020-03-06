# Create a simple `fastapi` application

[`fastapi`] is a web application framework in [Python]. It uses type annotations to define endspoints.

    import fastapi, click

Make an instance of a `fastapi` application.

    app = fastapi.FastAPI()


    @app.get('/highlight/{str}')
    def highlight_terminal(str:str):


        import pygments.formatters.terminal256
        return pygments.highlight(str, pygments.lexers.find_lexer_class_by_name('yaml')(), pygments.formatters.terminal256.Terminal256Formatter(style='bw'))

    @app.get('/upper/{str}')
    def upper(str:str):

`upper` returns the uppercase value of the input string.

return str.upper()

@click.group()
def cli(): ...

@cli.command()
def schema():

Display the `schema` for our simple application.

click.echo(highlight_terminal(**import**('yaml').safe_dump(app.openapi(), default_flow_style=False)))

@cli.command()
def serve():

Serve the simple `fastapi` application.

**import**('uvicorn').run(app, host="0.0.0.0", port=8000)

    __name__ == "__main__" and cli()

    def _test_app():
        __import__('nest_asyncio').apply()
        import starlette.testclient
        client = starlette.testclient.TestClient(app)
        assert client.get('/upper/rawr').text == 'RAWR!'

[`fastapi`]: #
[debuggery]: https://fastapi.tiangolo.com/tutorial/debugging/
