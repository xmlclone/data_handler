import sys

from enum import Enum
from typing import Optional, NewType, Dict, TypeVar, Union
from datetime import datetime
from pathlib import Path
from pydantic import field_serializer
from pydantic.dataclasses import dataclass

# TypeAlias 3.10
# Annotated 3.9

if sys.version_info <= (3, 9):
    str_30 = str
    str_100 = str
else:
    from typing import Annotated
    str_30 = Annotated[str, 30]
    str_100 = Annotated[str, 100]

if sys.version_info <= (3, 10):
    EmailFile = Union[str, Path]
    TemplateID = Union[int, str]
else:
    from typing import TypeAlias
    EmailFile: TypeAlias = str | Path
    TemplateID: TypeAlias = int | str


DictModel = NewType('DictModel', Dict)
JsonStrModel = NewType('JsonStrModel', str)

EmailUser = NewType('EmailUser', str)
SMSUser = TypeVar('SMSUser', str, int)
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