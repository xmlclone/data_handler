from typing import List, Optional
from datetime import datetime, date
from sqlalchemy import Column, JSON
from sqlalchemy.orm import mapped_column, Mapped
from pydantic import Field
from data_handler.models.base import DB_BASE, MD_BASE
from data_handler.dh_typing import (
    str_30,
    str_100,
    ResultEnum,
    Step,
)


class ExcutionRecordDB(DB_BASE):
    __tablename__ = 'excution_record'

    id: Mapped[int] = mapped_column(primary_key=True)
    # 项目名
    project: Mapped[str_30]
    # 场景名
    scene: Mapped[str_100]
    # 执行机所在区域
    area: Mapped[Optional[str_30]] = mapped_column(default='')
    # 测试步骤
    steps = Column('steps', JSON, nullable=False)
    # 场景启动时间
    start_time: Mapped[datetime]
    # 场景结束时间
    end_time: Mapped[datetime]
    # 结果
    result: Mapped[Optional[ResultEnum]] = mapped_column(default=ResultEnum.NotExecuted)
    # 错误消息
    error_message: Mapped[Optional[str]] = mapped_column(default='')

    # AI 相关记录
    ai_reason_code: Mapped[Optional[int]] = mapped_column(default=-1)
    ai_reason: Mapped[Optional[str]] = mapped_column(default='')
    act_reason_code: Mapped[Optional[int]] = mapped_column(default=-1)
    act_reason: Mapped[Optional[str]] = mapped_column(default='')

    # 执行日期，便于数据统计
    day: Mapped[date]


class ExcutionRecordModel(MD_BASE, extra='forbid'):
    id: Optional[int] = Field(exclude=True, default=0)
    project: str_30
    scene: str_100
    area: Optional[str_30] = ''
    steps: List[Step]
    start_time: datetime
    end_time: datetime
    result: ResultEnum = Field(default=ResultEnum.NotExecuted)
    error_message: Optional[str] = ''

    ai_reason_code: Optional[int] = -1
    ai_reason: Optional[str] = ''
    act_reason_code: Optional[int] = -1
    act_reason: Optional[str] = ''

    day: Optional[date] = date.today()
