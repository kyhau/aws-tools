import logging
from os import makedirs
from os.path import abspath, dirname


def init_logging(
    name="default",
    log_level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    log_file=None,
):
    """
    Initialise basic logging to console (and file).

    E.g. format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    """
    # logging.basicConfig(
    #     level=log_level,
    #     format=f"{log_time}%(levelname)-8s {package_name}: %(message)s",
    # )
    logging.getLogger().setLevel(log_level)
    logging.getLogger("botocore").setLevel(logging.CRITICAL)
    logging.getLogger("boto3").setLevel(logging.CRITICAL)
    logging.getLogger("urllib3.connectionpool").setLevel(logging.CRITICAL)

    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    formatter = logging.Formatter(format)

    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    if log_file is not None:
        makedirs(dirname(abspath(log_file)), exist_ok=True)

        fh = logging.FileHandler(log_file)
        fh.setLevel(log_level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger
