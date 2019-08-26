import click
import docker
import logging
from arki import init_logging


init_logging()


@click.command()
@click.option("--remove", "-r", is_flag=True, help="Remove non-running containers")
def find_non_running_containers(remove):
    """
    Find non-running containers.
    """

    client = docker.from_env()

    containers = client.containers.list(filters={"status": "exited"})
    logging.info(f"Found {len(containers)} non-running containers")
    if len(containers) > 0:
        print(f"ContainerId\tStatus\tImage")
        for c in containers:
            print(f"{c.short_id}\t{c.status}\t{c.image.tags}")

        if remove is True:
            for c in containers:
                try:
                    c.remove()
                except Exception as e:
                    logging.error(e)

            logging.info("Removed non-running images")


@click.command()
@click.option("--remove", "-r", is_flag=True, help="Remove dangling images")
def find_dangling_images(remove):
    """
    Find dangling images.
    """

    client = docker.from_env()

    images = client.images.list(filters={"dangling": True})
    logging.info(f"Found {len(images)} dangling images")
    if len(images) > 0:
        print("ID\t\tTags")
        for i in images:
            print(f"{i.id}\t{i.tags}")

        if remove:
            client.images.prune(filters={"dangling": True})
            logging.info("Removed dangling images")
