import logging

from typing import Optional, Union
from mgtg_msgntf.model import NotificationModel
from mgtg_msgntf.dh_typing import DictModel, JsonStrModel
from mgtg_msgntf.event import Events
from mgtg_msgntf.notify import Notify


class Environment:
    logger = logging.getLogger(__name__)

    def __init__(
        self,
        *,
        notify_config: Union[NotificationModel, DictModel, JsonStrModel],
        events: Optional[Events] = None,
    ) -> None:
        self.events = events or Events()
        self.notify_model: NotificationModel = self._2model(notify_config)
        self.notify = Notify()
        self.events.testcase_add.add_listener(self.notify.send_email)
        self.events.testcase_add.add_listener(self.notify.send_wx)
        # self.events.testcase_add.add_listener(self.notify.send_sms)

    def _dict2model(self, model: DictModel) -> NotificationModel:
        return NotificationModel.model_validate(model)

    def _str2model(self, model: JsonStrModel) -> NotificationModel:
        return NotificationModel.model_validate_json(model)

    def _2model(self, model: Union[NotificationModel, DictModel, JsonStrModel]) -> Union[NotificationModel, None]:
        _type = type(model)
        _model = None
        if _type == NotificationModel:
            _model = model
        elif _type == dict:
            _model = self._dict2model(model)
        elif _type == str:
            _model = self._str2model(model)
        self.logger.debug(f"notification model: {_model}")
        return _model
    
