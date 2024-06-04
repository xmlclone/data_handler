from enum import Enum
from typing import Annotated, Optional, NewType, Dict, IO, TypeAlias, TypeVar
from datetime import datetime
from pathlib import Path
from pydantic import field_serializer
from pydantic.dataclasses import dataclass


str_30 = Annotated[str, 30]
str_100 = Annotated[str, 100]


DictModel = NewType('DictModel', Dict)
JsonStrModel = NewType('JsonStrModel', str)

EmailUser = NewType('EmailUser', str)
EmailFile: TypeAlias = str | Path
SMSUser = TypeVar('SMSUser', bound=str|int)
WXUser = NewType('WXUser', str)


class ResultEnum(Enum):
    Failure = 'Failure'
    Success = 'Success'
    NotExecuted = 'NotExecuted'


@dataclass
class Step:
    id: int
    title: str_100
    start_time: datetime
    end_time: datetime
    result: ResultEnum
    error_message: Optional[str] = ''

    @field_serializer('start_time', 'end_time')
    def serializer_dt(self, dt: datetime, _info):
        return str(dt)
    
    @field_serializer('result')
    def serializer_result(self, result: ResultEnum, _info):
        return result.value