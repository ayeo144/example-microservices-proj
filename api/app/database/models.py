from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import JSONB

from app.database.db_admin import Base


class Task(Base):

    __tablename__ = "tbl_task"

    uuid = Column(String, primary_key=True)
    complete = Column(Boolean)
    process = Column(String)
    data = Column(JSONB)