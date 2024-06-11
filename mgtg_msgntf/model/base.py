from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session
from pydantic import BaseModel, ConfigDict
from mgtg_msgntf.settings import DB_URI


DB_ENGINE = create_engine(DB_URI, echo=False)
SESSION = Session(DB_ENGINE)


class DB_BASE(DeclarativeBase):
    ...


class MD_BASE(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
    )