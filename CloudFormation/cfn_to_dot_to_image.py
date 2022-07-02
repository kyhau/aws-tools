"""
Require:
sudo apt install graphviz
pip install cfn-lint pydot
pip install click
"""
from os import makedirs, rename, system
from os.path import basename, join

import click

import pydot


@click.command(help="Create DOT graph and png files for a CloudFormation template")
@click.argument("template")
@click.argument("output_dir")
def run(template, output_dir):
    makedirs(output_dir, exist_ok=True)

    print(f"Building DOT graph from the CloudFormation template {template}...")

    ret = system(f"cfn-lint {template} -g")
    if ret != 0:
       raise Exception("Failed to call cfn-lint")

    default_dot_file = f"{template}.dot"
    dot_file = join(output_dir, basename(default_dot_file))
    rename(default_dot_file, dot_file)

    print(f"Creating png...")

    png_file = join(output_dir, f"{basename(template)}.png")
    graph, = pydot.graph_from_dot_file(dot_file)
    graph.write_png(png_file)


if __name__ == "__main__":
     run()
