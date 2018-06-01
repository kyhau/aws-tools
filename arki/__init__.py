import click
import pkg_resources


@click.command()
def show_all_console_scripts(package_name="arki"):
    entrypoints = (
        ep for ep in pkg_resources.iter_entry_points("console_scripts")
        if ep.module_name.startswith(package_name)
    )
    for i in entrypoints:
        print(str(i).split("=")[0])
    return entrypoints
