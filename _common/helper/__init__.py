import logging
import os
from importlib.metadata import entry_points
from os.path import basename, dirname

PACKAGE_NAME = basename(dirname(__file__))


def print_all_console_scripts(package_name=PACKAGE_NAME):
    """
    Print all console scripts of a package.
    :param package_name: the name of a package installed.
    """
    print(f"Console scripts in {package_name}:")
    print("------------------------")

    # Get all console_scripts entry points
    eps = entry_points()

    # Handle both old dict-like and new SelectableGroups API
    if hasattr(eps, 'select'):
        # Python 3.10+ with SelectableGroups
        console_scripts = eps.select(group='console_scripts')
    else:
        # Fallback for older format (dict-like)
        console_scripts = eps.get('console_scripts', [])

    # Filter and print entry points for this package
    matching_entrypoints = []
    for ep in console_scripts:
        if ep.value.split(':')[0].startswith(package_name.lower()):
            print(ep.name)
            matching_entrypoints.append(ep)

    return matching_entrypoints


if __name__ == "__main__":
    print_all_console_scripts()
