import click
import os


@click.command()
@click.option("--directory", "-d", help="Directory of the query files.")
def main(directory):
    dir_path = directory if directory else os.path.dirname(os.path.realpath(__file__))
    for file in os.listdir(dir_path):
        if file.endswith(".txt"):
            print(os.path.join(dir_path, file))


if __name__ == "__main__": main()
