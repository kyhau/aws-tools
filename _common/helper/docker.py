import logging

import click
import docker
from helper.logger import init_logging

init_logging()
client = docker.from_env()


@click.command()
@click.option("--remove", "-r", is_flag=True, help="Remove non-running containers")
def find_non_running_containers(remove):
    """Find non-running containers."""

    containers = client.containers.list(filters={"status": "exited"})
    logging.info("Found %d non-running containers", len(containers))
    if len(containers) > 0:
        logging.info(f"ContainerId\tStatus\tImage")
        for c in containers:
            logging.info(f"{c.short_id}\t{c.status}\t{c.image.tags}")

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
    """Find dangling images."""

    images = client.images.list(filters={"dangling": True})
    logging.info("Found %d dangling images", len(images))
    if len(images) > 0:
        logging.info("ID\t\tTags")
        for i in images:
            logging.info(f"{i.id}\t{i.tags}")

        if remove:
            client.images.prune(filters={"dangling": True})
            logging.info("Removed dangling images")
