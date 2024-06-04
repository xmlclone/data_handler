from datetime import datetime
from data_handler.models.base import SESSION, DB_BASE, DB_ENGINE
from data_handler.models import ExcutionRecord, ExcutionRecordModel
from data_handler.dh_typing import Step, ResultEnum
from data_handler.services import ExcutionRecord


DB_BASE.metadata.drop_all(DB_ENGINE)
DB_BASE.metadata.create_all(DB_ENGINE)
print('-' * 100)


step1 = Step(
    id=1,
    title='test-step',
    start_time=datetime.now(),
    end_time=datetime.now(),
    result=ResultEnum.Success,
)

m = ExcutionRecordModel(
    project='test-project',
    scene='test-scene',
    steps=[step1],
    start_time=datetime.now(),
    end_time=datetime.now(),
    result=ResultEnum.Success
)

api = ExcutionRecord()
api.add(m)


step2 = Step(
    id=2,
    title='test-step2',
    start_time=datetime.now(),
    end_time=datetime.now(),
    result=ResultEnum.Success,
)

m2 = ExcutionRecordModel(
    project='test-project',
    scene='test-scene2',
    steps=[step1, step2],
    start_time=datetime.now(),
    end_time=datetime.now(),
    result=ResultEnum.Success
)

api.add_all([m, m2])
