import os
import logging
import warnings
import typing

from mgtg_msgntf.logger import config_log
from mgtg_msgntf.env import Environment
from mgtg_msgntf.dao import ExcutionRecord
from mgtg_msgntf.settings import LOG_PATH
from mgtg_msgntf.constant import ResultStatus, FailLevel
from mgtg_msgntf.event import events
from mgtg_msgntf.deco import catch_exception_to_developer

if typing.TYPE_CHECKING:
    from mgtg_msgntf.model import NotificationModel
    from mgtg_msgntf.dh_typing import JsonStrModel, DictModel


__all__ = [
    "ResultStatus",
    "FailLevel",
    "start_app",
]


try:
    os.makedirs(LOG_PATH, exist_ok=True)
except Exception as e:
    warnings.warn(e)


@catch_exception_to_developer
def start_app(
    *,
    notify_config: typing.Union["NotificationModel", "JsonStrModel", "DictModel"],
    console_log_level='info',
) -> ExcutionRecord:
    """启动程序，初始化相关参数并返回 `ExcutionRecord` 对象，后续可通过 `ExcutionRecord` 对象的 `add` 等方法增加记录数据

    :param notify_config: 消息通知配置，除邮件配置必选外，其它(微信、短信)均可选
    :type notify_config: `NotificationModel`、字典或json格式的字符串均可, 格式参考如下:

    ```
    {
        "email": [  # 邮件通知
            {
                "template_id": "template_1",       # type:str, 目前可选 1 2 3, 模板效果可自行验证查看
                "to_users": ["users1", "users2"],  # type: List[str] 需要接收邮件的邮箱列表
            },
            {
                "template_id": "template_2",
                "to_users": ["users1", "users3"], # 不同分组的发送的人员列表可以重复
                "cc_users": ["user2", "user4"], # 抄送人员，非必填
                "attachements": ["path/to/file1", "path/to/file2"] # 邮件附件，非必填
                # meta 可选，默认是 FailLevel.PageError FailLevel.SystemCrash ResultStatus.Failure 并且是or的关系
                "meta": {
                    "fail_level": [FailLevel.SystemCrash], # type: List[FailLevel]，失败等级
                    "result_status": [ResultStatus.Failure], # type: List[ResultStatus]，结果等级
                    "operator": "and"  # 可选 or 和 and, and表示上述两个条件均需要满足, or表示上述条件满足一个即可
                }
            },
        ],
        'wx': [ # 微信通知，非必填
            {
                "template_id": "template_1",  # 目前可选 1 2
                "to_users": ["users1", "users2"], # 微信用户ID, 可以找linlei获取
            },
            {
                "template_id": "template_2",
                "to_users": ["users3", "users4"],
            }
        ],
        'sms': [ # 短信通知，非必填
            {
                "template_id": "template_1",
                "to_users": ["users1", "users2"],
            },
            {
                "template_id": "template_2",
                "to_users": ["users3", "users4"],
            }
        ]
    }
    ```

    :param console_log_level: 控制台日志级别，默认 `info` ，可选 `debug` `info` `warning` `error` 等
    :type console_log_level: string

    :return: 返回 `ExcutionRecord` 对象
    :rtype: `ExcutionRecord`


    常用示例:


    1. 记录数据(默认情况下，记录数据中有失败，会触发 `notify_config` 所配置的通知)
    ```
    app = start_app(notify_config_dict)

    # 增加一条数据
    app.add(Union[ExcutionRecordModel, DictModel, JsonStrModel])

    # 也可以一次增加多条数据(不建议使用)
    app.add_all(List[Union[ExcutionRecordModel, DictModel, JsonStrModel]])
    ```


    2. 增加、删除事件
    ```
    # 目前系统 `testcase_add` 事件具有监听器 `Environment.send_email` 和 `Environment.send_wx` ，事件在记录数据时会触发消息通知
    # 但记录的数据需要满足 `Meta` 定义的规则:
    class Meta:
        # 不会针对单个步骤进行判断，只会对整个用例或场景判断
        # 单个列表里面元素之间是 or 的关系
        # 多个列表相互之间的关系需要通过 operator 指定
        fail_level: Optional[List[FailLevel]] = [FailLevel.PageError, FailLevel.SystemCrash]
        result_status: Optional[List[ResultStatus]] = [ResultStatus.Failure]
        # 表示上述等级的判断逻辑
        operator: Optional[Literal['or', 'and']] = 'or'

    app = start_app(notify_config_dict)

    # 事件可以移除
    app.env.events.testcase_add.remove_listener(app.env.send_email)

    # 也可以增加自定义事件，事件回调函数有两个参数，其类型如下
    def user_listener(model: ExcutionRecordModel, notify: NotificationModel):
        ...
    app.env.events.testcase_add.add_listener(user_listener)

    # 也可以在你想触发事件的地方主动触发事件的调用
    app.env.events.testcase_add.fire(ExcutionRecordModel, app.env.notify_model)
    ```
    """
    config_log(LOG_PATH, console_log_level)
    logger = logging.getLogger(__name__)
    logger.debug(f"start app, {notify_config=}")
    return ExcutionRecord(Environment(notify_config=notify_config, events=events))