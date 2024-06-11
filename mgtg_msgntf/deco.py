import logging
import traceback

from typing import Callable
from mgtg_msgntf.model.base import SESSION
from mgtg_msgntf.event import events
from mgtg_msgntf.exception import MgtgMsgtfError, MgtgDBError
from sqlalchemy.exc import OperationalError


logger = logging.getLogger(__name__)


def catch_exception_to_developer(target):
    def wrapper(*args, **kwargs):
        try:
            return target(*args, **kwargs)
        except Exception as e:
            logger.debug(e)
            logger.debug(traceback.format_exc())
            events.fw_exception.fire(e=e)
            raise MgtgMsgtfError('msg notify fw error, see the log file for detail.')
    return wrapper


def transaction(fn: Callable, commit=True, rollback=True):
    def wrapper(*args, **kwargs):
        try:
            result = fn(*args, **kwargs)
            logger.debug(f"call fn={fn.__qualname__} with {args=}, {kwargs=}, {commit=}, {rollback=}")
            if commit:
                SESSION.commit()
            return result
        except Exception as e:
            if rollback:
                SESSION.rollback()
            logger.debug(e)
            logger.debug(traceback.format_exc())
            events.fw_exception.fire(e=e)
            raise MgtgDBError('msg nofity db error.')
    return wrapper


