from datetime import datetime
from data_handler import start_app, ResultEnum


"""
需要依赖以下环境变量:

TG_EMAIL_HOST    mail.migu.cn
TG_EMAIL_PORT    25
TG_EMAIL_ACCOUNT 邮箱账号
TG_EMAIL_PASSWD  OA密码
"""


notify_config = {
    "email": [
        {
            "template_id": "1",
            "to_users": ["linlei@migu.cn"],
            "cc_users": ["linlei@migu.cn"], # 抄送人员，非必填
            # "attachements": ["path/to/file1", "path/to/file2"] # 邮件附件，非必填
        },
        # {
        #     "template_id": "2",
        #     "to_users": ["users1", "users3"], # 不同分组的发送的人员列表可以重复
        # },
    ],
    'wx': [ # 微信通知，非必填
        {
            "template_id": "1",
            "to_users": ["oYB6C6aG8NkiqFLyHhO9xsH9sHm0"],
        },
        # {
        #     "template_id": "2",
        #     "to_users": ["users3", "users4"],
        # }
    ],
    'sms': [ # 短信通知，非必填，当前也暂未实现
        {
            "template_id": "1",
            "to_users": ["users1", "users2"],
        },
        {
            "template_id": "2",
            "to_users": ["users3", "users4"],
        }
    ]
}


model = {
    "project": "test-project",
    "scene": "test-scene, max-length=30",
    "area": "成都",
    "steps": [
        {
            "id": "1",
            "title": "step 1",
            "start_time": datetime.now(),
            "end_time": datetime.now(),
            "result": ResultEnum.Success,
            "error_message": ""
        },
        {
            "id": "2",
            "title": "step 2",
            "start_time": datetime.now(),
            "end_time": datetime.now(),
            "result": ResultEnum.Failure,
            "error_message": "error message, optional"
        },
        {
            "id": "3",
            "title": "step 3",
            "start_time": datetime.now(),
            "end_time": datetime.now(),
            "result": ResultEnum.NotExecuted,
            "error_message": ""
        },
    ],
    "start_time": datetime.now(),
    "end_time": datetime.now(),
    "result": ResultEnum.Failure,
    "error_message": "error message, optional"
}

app = start_app(notify_config=notify_config, console_log_level='debug')
app.add(model)