import typer

cli = typer.Typer()

@cli.command()
def hello():
    print('hello')

@cli.command()
def world():
    print('world')
