import logging
import traceback

from typing import Callable
from data_handler.models.base import SESSION
from data_handler.event import events


logger = logging.getLogger(__name__)


def catch_exception_to_developer(target):
    def wrapper(*args, **kwargs):
        try:
            return target(*args, **kwargs)
        except Exception as e:
            logger.error(e)
            logger.debug(traceback.format_exc())
            events.fw_exception.fire(e=e)
            raise
    return wrapper


# @catch_exception_to_developer
def transaction(fn: Callable, commit=True, rollback=True):
    def wrapper(*args, **kwargs):
        try:
            result = fn(*args, **kwargs)
            logger.debug(f"call fn={fn.__qualname__} with {args=}, {kwargs=}, {commit=}, {rollback=}")
            if commit:
                SESSION.commit()
            return result
        except:
            if rollback:
                SESSION.rollback()
            raise
    return wrapper


