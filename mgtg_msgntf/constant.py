from enum import Enum


class ResultStatus(Enum):
    Failure = 'Failure'
    Success = 'Success'
    NotExecuted = 'NotExecuted'


class FailLevel(Enum):
    NonFail = 'NonFail'
    SystemCrash = 'SystemCrash'
    PageError = 'PageError'
    NonFunctionlError = 'NonFunctionlError'