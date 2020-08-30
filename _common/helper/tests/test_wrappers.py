import logging

from helper.wrappers import init_wrapper


@init_wrapper
def process(*args, **kwargs):
    logging.debug("At function process()")
    assert kwargs.get("data") == [1, 2, 3]
    return 12345

def test_init_wrapper_succeeded():
    assert process(data=[1, 2, 3]) == 12345

def test_init_wrapper_failed():
    assert process(data=[1, 2]) == 1
