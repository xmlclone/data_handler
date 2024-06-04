import traceback

from datetime import datetime
from sqlalchemy import select
from data_handler.models import ExcutionRecordDB, ExcutionRecordModel
from data_handler.dh_typing import Step, ResultEnum
from data_handler.models.base import SESSION, DB_BASE, DB_ENGINE


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
print(m)

o = ExcutionRecordDB(**m.model_dump())
print(o)
SESSION.add(o)
SESSION.commit()

result = SESSION.scalars(
    select(ExcutionRecordDB)
).one()
print(result)

m: ExcutionRecordModel = ExcutionRecordModel.model_validate(result)
print(m)
print(type(m.steps[0].start_time))

