from typing import List, Optional
from datetime import datetime, date
from sqlalchemy import Column, JSON
from sqlalchemy.orm import mapped_column, Mapped
from pydantic import Field, field_serializer
from mgtg_msgntf.model.base import DB_BASE, MD_BASE
from mgtg_msgntf.constant import ResultStatus, FailLevel
from pydantic.dataclasses import dataclass
from mgtg_msgntf.dh_typing import (
    str_30,
    str_100,
)


@dataclass
class PageMetaData:
    action: str # 操作行为
    action_element: str # 操作的元素


@dataclass
class Step:
    id: int
    title: str_100
    start_time: datetime
    end_time: datetime
    result_status: ResultStatus
    error_message: Optional[str] = ''
    debug_message: Optional[str] = ''
    fail_level: Optional[FailLevel] = FailLevel.NonFail
    meta_data: Optional[PageMetaData] = None

    @field_serializer('start_time', 'end_time')
    def serializer_dt(self, dt: datetime, _info):
        return str(dt)
    
    @field_serializer('result_status')
    def serializer_result(self, result_status: ResultStatus, _info):
        return result_status.value
    
    @field_serializer('fail_level')
    def serializer_fail_level(self, fail_level: FailLevel, _info):
        return fail_level.value


class ExcutionRecordDB(DB_BASE):
    __tablename__ = 'excution_record'

    id: Mapped[int] = mapped_column(primary_key=True)
    # 业务方
    # 1 咪咕探针 2 拨测框架
    bus_id: Mapped[int]
    # 项目名
    project: Mapped[str_30]
    # 场景名 --- 可对应某个页面或功能模块
    scene: Mapped[str_100]
    # 执行机所在区域
    area: Mapped[Optional[str_30]] = mapped_column(default='')
    # 测试步骤
    steps = Column('steps', JSON, nullable=True)
    # 场景启动时间
    start_time: Mapped[datetime]
    # 场景结束时间
    end_time: Mapped[datetime]
    # 结果
    result_status: Mapped[Optional[ResultStatus]] = mapped_column(default=ResultStatus.NotExecuted)
    # 错误消息
    error_message: Mapped[Optional[str]] = mapped_column(default='')
    # debug信息
    debug_message: Mapped[Optional[str]] = mapped_column(default='')
    # 失败等级
    fail_level: Mapped[Optional[FailLevel]] = mapped_column(default=FailLevel.NonFail)

    # AI 相关记录
    ai_reason_code: Mapped[Optional[int]] = mapped_column(default=-1)
    ai_reason: Mapped[Optional[str]] = mapped_column(default='')
    act_reason_code: Mapped[Optional[int]] = mapped_column(default=-1)
    act_reason: Mapped[Optional[str]] = mapped_column(default='')

    # 执行日期，便于数据统计
    day: Mapped[date]


class ExcutionRecordModel(MD_BASE, extra='forbid'):
    id: Optional[int] = Field(exclude=True, default=0)
    # 1 咪咕探针 2 拨测框架
    bus_id: int
    project: str_30
    scene: str_100
    area: Optional[str_30] = ''
    steps: Optional[List[Step]] = []
    start_time: datetime
    end_time: datetime
    result_status: ResultStatus = Field(default=ResultStatus.NotExecuted)
    error_message: Optional[str] = ''
    debug_message: Optional[str] = ''
    fail_level: Optional[FailLevel] = Field(default=FailLevel.NonFail)

    ai_reason_code: Optional[int] = -1
    ai_reason: Optional[str] = ''
    act_reason_code: Optional[int] = -1
    act_reason: Optional[str] = ''

    day: Optional[date] = date.today()
