from typer import Typer


app = Typer(name='ec2')


@app.command()
def list():
    print('ec2 instance list')


@app.command()
def show():
    print('ec2 instance show')
