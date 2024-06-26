from datetime import datetime
from mgtg_msgntf import start_app, ResultStatus, FailLevel


"""
使用前，请先使用命令初始化环境: 
python -m mgtg_msgntf.__main__ init-db

并配置以下环境变量:
TG_EMAIL_HOST    mail.migu.cn
TG_EMAIL_PORT    25
TG_EMAIL_ACCOUNT 邮箱账号  --- 配置自己的邮箱账号
TG_EMAIL_PASSWD  OA密码
"""


# 通知模板
notify_config = {
    "email": [
        {
            "template_id": "3",
            "to_users": ["linlei@migu.cn"],
            # "cc_users": ["linlei@migu.cn"], # 抄送人员，非必填
            # "attachements": ["path/to/file1", "path/to/file2"] # 邮件附件，非必填
        },
        {
            "template_id": "3",
            "to_users": ["linlei@migu.cn"], # 不同分组的发送的人员列表可以重复
            # 并且可以配置通知告警级别
            "meta": {
                "fail_level": [FailLevel.SystemCrash], # type: List[FailLevel]，失败等级
                "result_status": [ResultStatus.Failure], # type: List[ResultStatus]，结果等级
                "operator": "and"  # 可选 or 和 and, and表示上述两个条件均需要满足, or表示上述条件满足一个即可
            }
        },
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


# 数据模板
model = {
    "project": "test-project, max-length=30",
    "bus_id": 1,  # 咪咕探针，固定传1
    "scene": "test-scene, max-length=100",   # test case name or scene name
    "area": "成都",
    "steps": [ # can be ignore
        {
            "id": "1",
            "title": "step 1",
            "start_time": datetime.now(),
            "end_time": datetime.now(),
            "result_status": ResultStatus.Success,
            "error_message": "",
            "debug_message": "",
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
    "debug_message": "debug message, optional",
    "fail_level": FailLevel.PageError
}

app = start_app(notify_config=notify_config, console_log_level='info')

# 增加一条数据
app.add(model)