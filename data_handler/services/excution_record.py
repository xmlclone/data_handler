import logging

from typing import List, Union, Optional
from data_handler.models.base import SESSION
from data_handler.models import ExcutionRecordDB, ExcutionRecordModel, NotificationModel
from data_handler.decorator import transaction, catch_exception_to_developer
from data_handler.dh_typing import DictModel, JsonStrModel, ResultEnum
from data_handler.env import Environment


# @catch_exception_to_developer
class ExcutionRecord:
    logger = logging.getLogger(__name__)


    def __init__(self, env: Environment):
        self.env = env

    @transaction
    def add(self, model: Union[ExcutionRecordModel, DictModel, JsonStrModel]) -> None:
        """记录执行数据

        :param model: 执行数据模型
        :type model: `ExcutionRecordModel`、字典或json格式的字符串均可，格式参考如下：

        ```
        {
            "project": "test-project",
            "scene": "test-scene, max-length=30",
            "area": "machine area",
            "steps": [
                {
                    "id": "1",
                    "title": "step 1",
                    "start_time": "step start time, type: datetime",
                    "end_time": "step end time, type: datetime",
                    "result": "step result, type: ResultEnum",
                    "error_message": "error message, optional"
                },
                {
                    "id": "2",
                    "title": "step 2",
                    "start_time": "step start time, type: datetime",
                    "end_time": "step end time, type: datetime",
                    "result": "step result, type: ResultEnum",
                    "error_message": "error message, optional"
                },
            ],
            "start_time": "scene start time, type: datetime",
            "end_time": "scene end time, type: datetime",
            "result": "scene result, type: ResultEnum",
            "error_message": "error message, optional"
        }
        ```
        """
        _model = self._2model(model)
        if _model == None:
            return
        obj = self._model2db(_model)
        if _model.result == ResultEnum.Failure:
            self.env.events.testcase_fail.fire(model=_model, notify=self.env.notify_model)
        SESSION.add(obj)

    @transaction
    def add_all(self, models: List[Union[ExcutionRecordModel, DictModel, JsonStrModel]]) -> None:
        _models = [self._2model(model) for model in models]
        if not _models:
            return
        objs = []
        for model in _models:
            if model.result == ResultEnum.Failure:
                self.env.events.testcase_fail.fire(model=model, notify=self.env.notify_model)
            objs.append(self._model2db(model))
        SESSION.add_all(objs)

    def _model2db(self, model: ExcutionRecordModel) -> ExcutionRecordDB:
        return ExcutionRecordDB(**model.model_dump())

    def _dict2model(self, model: DictModel) -> ExcutionRecordModel:
        return ExcutionRecordModel.model_validate(model)

    def _str2model(self, model: JsonStrModel) -> ExcutionRecordModel:
        return ExcutionRecordModel.model_validate_json(model)

    def _2model(self, model: Union[ExcutionRecordModel, DictModel, JsonStrModel]) -> Union[ExcutionRecordModel, None]:
        _type = type(model)
        _model = None
        if _type == ExcutionRecordModel:
            _model = model
        elif _type == dict:
            _model = self._dict2model(model)
        elif _type == str:
            _model = self._str2model(model)
        self.logger.debug(f"excution record model: {_model}")
        return _model