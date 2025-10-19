import logging
from functools import wraps


def init_wrapper(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("At wrapper")
        logging.debug(kwargs)

        # app_name = kwargs.get("app_name")
        # config_file = kwargs.get("config_file")

        try:
            logging.debug("Start running actual function")
            return_code = func(*args, **kwargs)

        except Exception as e:
            import traceback

            traceback.print_stack()
            logging.error(e)
            return_code = 1

        return return_code

    return wrapper
