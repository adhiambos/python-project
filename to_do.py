from sqlalchemy import create_engine, Column, Integer, String, ForeignKey,UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    tasks = relationship("Task", backref="user")

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    subtasks = relationship("Subtask", backref="task")

class Subtask(Base):
    __tablename__ = 'subtasks'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    task_id = Column(Integer, ForeignKey('tasks.id'))
    __table_args__ = (UniqueConstraint('task_id', 'title', name='unique_subtask'),)
  

