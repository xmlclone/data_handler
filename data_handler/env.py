import logging

from datetime import datetime
from typing import Optional, Union
from data_handler.models import NotificationModel, ExcutionRecordModel
from data_handler.dh_typing import DictModel, JsonStrModel
from data_handler.event import Events
from data_handler.apis import Email, WX, SMS


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
        self.events.testcase_fail.add_listener(self.notify)

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
    
    def notify(self, model: ExcutionRecordModel, notify: NotificationModel):
        self.logger.debug(f"notify called.")
        self.email, self.wx, self.sms = Email(), WX(), SMS()

        notify_dict = {
            "project": model.project,
            "testcase": model.scene,
            "starttime": model.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "area": model.area,
            "message": model.error_message,
            "airesult": "No"
        }

        for e in notify.email:
            subject = e.template_id['subject']
            content = e.template_id['content']
            self.email.send(
                e.to_users,
                subject.format(project=model.project),
                content.format(**notify_dict),
                e.cc_users,
                e.attachements or {}
            )

        for w in notify.wx:
            self.wx.send(w.to_users, w.template_id, notify_dict)

        for s in notify.sms:
            self.sms.send(s.to_users)

    
