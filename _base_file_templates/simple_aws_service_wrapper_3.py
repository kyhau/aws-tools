import click


@click.group(invoke_without_command=True, help="TODO Help 1")
@click.pass_context
def main_cli(ctx):
    if ctx.invoked_subcommand is not None:
        click.echo('I am about to invoke %s' % ctx.invoked_subcommand)
        return
    click.echo('I was invoked without subcommand')


@main_cli.command(help="TODO cmd1")
@click.argument("var1", type=click.STRING)
@click.pass_context
def cmd1(ctx, var1):
    ctx.ensure_object(dict)
    click.echo(f"cmd1: {var1}, {ctx.obj}")


@main_cli.command(help="TODO cmd2")
@click.argument("var2", type=click.STRING)
@click.pass_context
def cmd2(ctx, var2):
    click.echo(f"cmd2: {var2}, {ctx.obj}")


if __name__ == "__main__":
    main_cli(obj={"debug": "true"})
