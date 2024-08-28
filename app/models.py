from datetime import datetime
from sqlalchemy import Column, DateTime, Enum, Integer, Interval
from sqlalchemy.ext.declarative import declarative_base

from app.enum import TaskStatus

Base = declarative_base()


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.IN_QUEUE)
    create_time = Column(DateTime, default=datetime.now())
    start_time = Column(DateTime, nullable=True)
    exec_time = Column(Interval, nullable=True)
