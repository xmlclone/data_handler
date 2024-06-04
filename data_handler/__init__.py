import os
import logging
import warnings
import typing
import traceback

from data_handler.logger import config_log
from data_handler.env import Environment
from data_handler.services import ExcutionRecord
from data_handler.settings import LOG_PATH
from data_handler.dh_typing import ResultEnum
from data_handler.event import events
from data_handler.decorator import catch_exception_to_developer

if typing.TYPE_CHECKING:
    from data_handler.models import NotificationModel
    from data_handler.dh_typing import JsonStrModel, DictModel


__all__ = [
    "ResultEnum",
    "start_app",
]


try:
    os.makedirs(LOG_PATH, exist_ok=True)
except Exception as e:
    warnings.warn(e)


# @catch_exception_to_developer
def start_app(
    *,
    notify_config: typing.Union["NotificationModel", "JsonStrModel", "DictModel"],
    console_log_level='info',
) -> ExcutionRecord:
    """启动程序，初始化相关参数并返回 `ExcutionRecord` 对象，后续可通过 `ExcutionRecord` 对象的 `add` 等方法增加记录数据

    :param notify_config: 消息通知配置，除邮件配置必选外，其它(微信、短信)均可选
    :type notify_config: `NotificationModel`、字典或json格式的字符串均可，格式参考如下：

    ```
    {
        "email": [
            {
                "template_id": "template_1",
                "to_users": ["users1", "users2"],
            },
            {
                "template_id": "template_2",
                "to_users": ["users1", "users3"], # 不同分组的发送的人员列表可以重复
                "cc_users": ["user2", "user4"], # 抄送人员，非必填
                "attachements": ["path/to/file1", "path/to/file2"] # 邮件附件，非必填
            },
        ],
        'wx': [ # 微信通知，非必填
            {
                "template_id": "template_1",
                "to_users": ["users1", "users2"],
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

    # 也可以一次增加多条数据
    app.add_all(List[Union[ExcutionRecordModel, DictModel, JsonStrModel]])
    ```


    2. 增加、删除事件
    ```
    # 目前系统 `testcase_fail` 事件具有唯一监听器是 `Environment.notify` ，此事件在记录数据中有失败时会出发消息通知
    app = start_app(notify_config_dict)

    # 事件可以移除
    app.env.events.testcase_fail.remove_listener(app.env.notify)

    # 也可以增加自定义事件，事件回调函数有两个参数，其类型如下
    def user_listener(model: ExcutionRecordModel, notify: NotificationModel):
        ...
    app.env.events.testcase_fail.add_listener(user_listener)

    # 也可以在你想触发事件的地方主动触发事件的调用
    app.env.events.testcase_fail.fire(ExcutionRecordModel, app.env.notify_model)
    ```
    """
    config_log(LOG_PATH, console_log_level)
    logger = logging.getLogger(__name__)
    logger.debug(f"start app, {notify_config=}")
    return ExcutionRecord(Environment(notify_config=notify_config, events=events))