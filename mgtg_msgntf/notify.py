import warnings
import logging

from typing import Union, Dict, cast
from mgtg_msgntf.model import NotificationModel, ExcutionRecordModel
from mgtg_msgntf.model.notification import SMSModel, WxModel, EmailModel
from mgtg_msgntf.apis import Email, WX, SMS


class Notify:
    logger = logging.getLogger(__name__)

    def __init__(self) -> None:
        self.email, self.wx, self.sms = Email(), WX(), SMS()

    def is_notify(self, model: ExcutionRecordModel, notify: Union[SMSModel, WxModel, EmailModel]) -> bool:
        result_status = False
        fail_level = False
        if model.result_status in notify.meta.result_status:
            result_status = True
        if model.fail_level in notify.meta.fail_level:
            fail_level = True
        express = f"{fail_level} {notify.meta.operator} {result_status}"
        self.logger.debug(f"{model=}, {notify=}")
        result = cast(bool, eval(express))
        self.logger.debug(f"{express=}, {result=}")
        return result
    
    def format_model(self, model: ExcutionRecordModel) -> Dict:
        warning_data = {
            "project": model.project,
            "bus_id": model.bus_id,
            "testcase": model.scene,
            "starttime": model.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "area": model.area,
            "message": model.error_message,
            "airesult": model.ai_reason,
            "level": model.fail_level,
            "debug_message": model.debug_message,
        }
        return warning_data

    def send_email(self, model: ExcutionRecordModel, notify: NotificationModel):
        warning_data = self.format_model(model)
        for email in notify.email:
            if not self.is_notify(model, email):
                continue
            subject = email.template_id['subject']
            content = email.template_id['content']
            self.email.send(
                email.to_users,
                subject.format(**warning_data),
                content.format(**warning_data),
                email.cc_users,
                email.attachements or {}
            )

    def send_wx(self, model: ExcutionRecordModel, notify: NotificationModel):
        warning_data = self.format_model(model)
        for wx in notify.wx:
            if not self.is_notify(model, wx):
                continue
            self.wx.send(wx.to_users, wx.template_id, warning_data)

    def send_sms(self, model: ExcutionRecordModel, notify: NotificationModel):
        warnings.warn("SMS warning not implemented.")
