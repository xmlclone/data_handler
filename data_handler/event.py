import logging
import traceback
import warnings

from data_handler.apis import WX


class EventHook:
    def __init__(self):
        self._handlers = []

    def add_listener(self, handler):
        self._handlers.append(handler)
        return handler

    def remove_listener(self, handler):
        self._handlers.remove(handler)

    def fire(self, *, reverse=False, **kwargs):
        if reverse:
            handlers = reversed(self._handlers)
        else:
            handlers = self._handlers
        for handler in handlers:
            try:
                handler(**kwargs)
            except Exception:
                logging.error("Uncaught exception in event handler: \n%s", traceback.format_exc())


class DeprecatedEventHook(EventHook):
    def __init__(self, message):
        self.message = message
        logging.warning(self.message)
        super().__init__()

    def add_listener(self, handler):
        logging.warning(self.message)
        return super().add_listener(handler)


class Events:
    """事件类"""


    """用例/场景失败
    :param model data_handler.models.ExcutionRecordModel
    :param notify data_handler.models.NotificationModel
    """
    testcase_fail: EventHook

    """框架异常
    :param e Exception
    """
    fw_exception: EventHook


    def __init__(self):
        for name, value in vars(type(self)).items():
            if value == EventHook:
                setattr(self, name, value())
            elif value == DeprecatedEventHook:
                setattr(self, name, value(f"{name} Event is DEPRECATED."))

        for name, value in self.__annotations__.items():
            if value == EventHook:
                setattr(self, name, value())
            elif value == DeprecatedEventHook:
                setattr(self, name, value(f"{name} Event is DEPRECATED."))


events = Events()


def fw_exception_callback(e: Exception):
    warnings.warn(e)
    WX().notify_devoloper(f"{e}\n{traceback.format_exc()}")


events.fw_exception.add_listener(fw_exception_callback)
