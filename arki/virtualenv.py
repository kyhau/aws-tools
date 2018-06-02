"""
This utility script creates virtualenv of a Python version to the current platform.
"""
import click
import sys
from arki import system


CMD_STR = "virtualenv -p {} {}"

@click.command()
@click.argument("python_version", required=True)
@click.option("--name", "-n", required=False, help="Name of the virtualenv name. Default: e.g. env_36 (Linux), env_36_win (Windows)")
def create(python_version, name):
    """
    Create virtualenv of the specified Python version (PYTHON_VERSION, e.g. 2.7, 3.4, 3.6) to the
    current platform (Linux or Windows).

    If --name is not specified, the name is env_(version_digit_only) on Linux, or
    env_(version_digit_only)_win on Windows."
    """

    ret_code = 0
    try:
        version_digit_only = python_version.replace(".","")

        if system.is_linux():
            venv_name = name if name else f"env_{version_digit_only}"

            create_cmd = CMD_STR.format(
                f"python{python_version}",
                venv_name
            )

            activate_cmd = f". {venv_name}/bin/activate"

        elif system.is_windows():
            venv_name = name if name else f"env_{version_digit_only}_win"

            create_cmd = CMD_STR.format(
                f"C:\\Python{version_digit_only}\python.exe",
                venv_name
            )

            activate_cmd = f"{venv_name}\\Scripts\\activate"

        else:
            raise Exception("Platform not supported")

        ret_code = system.run_command(create_cmd)

        if ret_code == 0:
            print("Activate environment with command:")
            print("----------------------------------")
            print(activate_cmd)
            print("----------------------------------")

    except Exception as e:
        print(f"Error: {e}")
        ret_code = 1

    sys.exit(ret_code)
