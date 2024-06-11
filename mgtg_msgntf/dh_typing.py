import sys

from typing import NewType, Dict, TypeVar, Union
from pathlib import Path

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
