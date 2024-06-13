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

engine = create_engine('sqlite:///todo.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

Session = sessionmaker(bind=engine)
session = Session()

def add_user(name):
    user = User(name=name)
    session.add(user)
    session.commit()
    return user

def add_task(title, user):
    task = Task(title=title, user=user)
    session.add(task)
    session.commit()
    return task

def add_subtask(title, task):
    try:
        subtask = Subtask(title=title, task=task)
        session.add(subtask)
        session.commit()
        return subtask
    except Exception as e:
        print(f"Failed to add subtask:{e}")
        return None


  

