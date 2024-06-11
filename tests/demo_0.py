from datetime import datetime
from mgtg_msgntf import start_app, ResultStatus, FailLevel


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
            # "cc_users": ["linlei@migu.cn"], # 抄送人员，非必填
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
    "bus_id": 1,  # 咪咕探针，固定传1
    "scene": "test-scene, max-length=30",   # test case name or scene name
    "area": "成都",
    "steps": [ # can be ignore
        {
            "id": "1",
            "title": "step 1",
            "start_time": datetime.now(),
            "end_time": datetime.now(),
            "result_status": ResultStatus.Success,
            "error_message": "",
            "fail_level": FailLevel.NonFail,
            "meta_data": {
                "action": "what action",
                "action_element": "which element"
            }
        },
        {
            "id": "2",  # 测试步骤，可以只有1个，只有1个步骤的适用场景: 步骤就是场景
            "title": "step 2",
            "start_time": datetime.now(),
            "end_time": datetime.now(),
            "result_status": ResultStatus.Failure,
            "error_message": "error message, optional",
            "fail_level": FailLevel.PageError,
            "meta_data": {
                "action": "what action",
                "action_element": "which element"
            }
        },
        {
            "id": "3",
            "title": "step 3",
            "start_time": datetime.now(),
            "end_time": datetime.now(),
            "result_status": ResultStatus.NotExecuted,
            "error_message": "",
            "fail_level": FailLevel.NonFail,
            "meta_data": {
                "action": "what action",
                "action_element": "which element"
            }
        },
    ],
    "start_time": datetime.now(),
    "end_time": datetime.now(),
    "result_status": ResultStatus.Failure,
    "error_message": "error message, optional",
    "fail_level": FailLevel.PageError
}

app = start_app(notify_config=notify_config, console_log_level='info')
app.add(model)