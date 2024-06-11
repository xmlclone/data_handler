from typing import List, Optional, Literal, Union
from pydantic.dataclasses import dataclass
from pydantic import field_validator, Field, BaseModel
from mgtg_msgntf.model.base import MD_BASE
from mgtg_msgntf.dh_typing import EmailUser, EmailFile, SMSUser, WXUser, TemplateID
from mgtg_msgntf.constant import FailLevel, ResultStatus


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

EMAIL_TEMPLATE2 = {
    "subject": """f[拨测告警][{project}][{airesult}]""",
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
"""
}



SMS_TEMPLAET1 = {}


@dataclass
class Meta:
    # 不会针对单个步骤进行判断，只会对整个用例或场景判断
    # 单个列表里面元素之间是 or 的关系
    # 多个列表相互之间的关系需要通过 operator 指定
    fail_level: Optional[List[FailLevel]] = Field(default_factory=lambda: [FailLevel.PageError, FailLevel.SystemCrash])
    # [FailLevel.PageError, FailLevel.SystemCrash]
    result_status: Optional[List[ResultStatus]] = Field(default_factory=lambda: [ResultStatus.Failure])
    # 表示上述等级的判断逻辑
    operator: Optional[Literal['or', 'and']] = 'or'


class BaseNtModel(BaseModel):
    template_id: TemplateID
    to_users: List[Union[EmailUser, WXUser, SMSUser]]
    meta: Optional[Meta] = Meta()


class EmailModel(BaseNtModel):
    cc_users: Optional[List[EmailUser]] = None
    attachements: Optional[List[EmailFile]] = None
    
    @field_validator('template_id')
    @classmethod
    def convert_tid(cls, tid: TemplateID) -> str:
        itid = int(tid)
        if itid == 1:
            return EMAIL_TEMPLATE1
        if itid == 2:
            return EMAIL_TEMPLATE2
        

class SMSModel(BaseNtModel):
    pass


class WxModel(BaseNtModel):
    @field_validator('template_id')
    @classmethod
    def convert_tid(cls, tid: TemplateID) -> str:
        itid = int(tid)
        if itid == 1:
            return '7PakBXJdWj_DES5AZHxAF6NTajDID_riqhA9TtkkwUU'
        if itid == 2:
            return 'b5GeMj60Az_xQ1iowYCqjiY_Vu0_055utiPchaQDinU'


class NotificationModel(MD_BASE, extra='forbid'):
    email: List[EmailModel]
    sms: Optional[List[SMSModel]] = None
    wx: Optional[List[WxModel]] = None