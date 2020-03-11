My document recieved {{sys.argv}} as arguments.

<!--

    print(__name__)

    import sys, click
    @click.command()
    def main():
        click.echo('The document was run as a CLI!')

    '__file__' in locals() and __name__ == '__main__' and main()

-->
