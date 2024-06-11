import logging

from typing import List, Union
from mgtg_msgntf.model.base import SESSION
from mgtg_msgntf.model import ExcutionRecordDB, ExcutionRecordModel
from mgtg_msgntf.deco import transaction
from mgtg_msgntf.dh_typing import DictModel, JsonStrModel
from mgtg_msgntf.env import Environment


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
            "bus_id": 1,
            "scene": "test-scene, max-length=30",
            "area": "machine area",
            "steps": [
                {
                    "id": "1",
                    "title": "step 1",
                    "start_time": "step start time, type: datetime",
                    "end_time": "step end time, type: datetime",
                    "result": "step result, type: ResultStatus",
                    "error_message": "error message, optional",
                    "fail_level": "fail level, type: FailLevel",
                    "meta_data": {
                        "action": "what action",
                        "action_element": "which element"
                    }
                },
                {
                    "id": "2",
                    "title": "step 2",
                    "start_time": "step start time, type: datetime",
                    "end_time": "step end time, type: datetime",
                    "result": "step result, type: ResultStatus",
                    "error_message": "error message, optional",
                    "fail_level": "fail level, type: FailLevel",
                    "meta_data": {
                        "action": "what action",
                        "action_element": "which element"
                    }
                },
            ],
            "start_time": "scene start time, type: datetime",
            "end_time": "scene end time, type: datetime",
            "result": "scene result, type: ResultStatus",
            "error_message": "error message, optional",
            "fail_level": "fail level, type: FailLevel",
        }
        ```
        """
        _model = self._2model(model)
        if _model == None:
            return
        obj = self._model2db(_model)
        self.env.events.testcase_add.fire(model=_model, notify=self.env.notify_model)
        SESSION.add(obj)

    def add_all(self, models: List[Union[ExcutionRecordModel, DictModel, JsonStrModel]]) -> None:
        # 因为需要监听单个对象，故未使用 SESSION.add_all()
        for model in models:
            self.add(model)

    def _model2db(self, model: ExcutionRecordModel) -> ExcutionRecordDB:
        return ExcutionRecordDB(**model.model_dump())

    def _dict2model(self, model: DictModel) -> ExcutionRecordModel:
        return ExcutionRecordModel.model_validate(model)

    def _str2model(self, model: JsonStrModel) -> ExcutionRecordModel:
        return ExcutionRecordModel.model_validate_json(model)

    def _2model(self, model: Union[ExcutionRecordModel, DictModel, JsonStrModel]) -> Union[ExcutionRecordModel, None]:
        _type = type(model)
        _model = None
        self.logger.debug(f"{model=}")
        if _type == ExcutionRecordModel:
            _model = model
        elif _type == dict:
            _model = self._dict2model(model)
        elif _type == str:
            _model = self._str2model(model)
        self.logger.debug(f"excution record model: {_model}")
        return _model