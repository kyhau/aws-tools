import click


@click.group(help="Help 1")
def cli1():
    pass


@cli1.command(help="A command to print environment variables")
@click.argument("envvar", type=click.STRING)
def cmd1(envvar):
    click.echo(f"Chosen envvar is {envvar}")


@cli1.command(help="A command to do something with user")
@click.argument("user", type=click.STRING)
def cmd2(user):
    click.echo(f"Chosen user is {user}")


if __name__ == "__main__":
    cli1()
