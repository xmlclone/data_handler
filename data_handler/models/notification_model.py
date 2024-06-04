from typing import List, Optional
from pydantic.dataclasses import dataclass
from pydantic import field_validator
from data_handler.models.base import MD_BASE
from data_handler.dh_typing import EmailUser, EmailFile, SMSUser, WXUser


EMAIL_TEMPLATE1 = {
    "subject": """[探针告警][{project}]""",
    "content": """
<html>
    <body style="width: 800px">
        <ul>
            <li style="margin-top: 8px;">项目名称: {project}</li>
            <li style="margin-top: 8px;">测试用例: {testcase}</li>
            <li style="margin-top: 8px;">执行时间: {starttime}</li>
            <li style="margin-top: 8px;">告警区域: {area}</li>
            <li style="margin-top: 8px;">失败消息: {message}</li>
            <li style="margin-top: 8px;">AI预分析(试运行): {airesult}</li>
        </ul>
    </body>
</html>
""",
}


SMS_TEMPLAET1 = {}


@dataclass
class EmailModel:
    template_id: int | str
    to_users: List[EmailUser]
    cc_users: Optional[List[EmailUser]] = None
    attachements: Optional[List[EmailFile]] = None

    @field_validator('template_id')
    @classmethod
    def convert_tid(cls, tid: int | str) -> str:
        if int(tid) == 1:
            return EMAIL_TEMPLATE1


@dataclass
class SMSModel:
    template_id: int | str
    to_users: List[SMSUser]


@dataclass
class WxModel:
    template_id: int | str
    to_users: List[WXUser]

    @field_validator('template_id')
    @classmethod
    def convert_tid(cls, tid: int | str) -> str:
        if int(tid) == 1:
            # return 'b5GeMj60Az_xQ1iowYCqjiY_Vu0_055utiPchaQDinU'
            return '7PakBXJdWj_DES5AZHxAF6NTajDID_riqhA9TtkkwUU'


class NotificationModel(MD_BASE, extra='forbid'):
    email: List[EmailModel]
    sms: Optional[List[SMSModel]] = None
    wx: Optional[List[WxModel]] = None