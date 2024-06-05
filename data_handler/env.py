import logging
import warnings

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
        self.email, self.wx, self.sms = Email(), WX(), SMS()
        self.events.testcase_fail.add_listener(self.warning_email)
        self.events.testcase_fail.add_listener(self.warning_wx)
        # self.events.testcase_fail.add_listener(self.warning_sms)

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
    
    def warning_email(self, model: ExcutionRecordModel, notify: NotificationModel):
        warning_data = {
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
                content.format(**warning_data),
                e.cc_users,
                e.attachements or {}
            )

    def warning_wx(self, model: ExcutionRecordModel, notify: NotificationModel):
        warning_data = {
            "project": model.project,
            "testcase": model.scene,
            "starttime": model.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "area": model.area,
            "message": model.error_message,
            "airesult": "No"
        }
        for w in notify.wx:
            self.wx.send(w.to_users, w.template_id, warning_data)

    def warning_sms(self, model: ExcutionRecordModel, notify: NotificationModel):
        warnings.warn("SMS warning not implemented.")

    
