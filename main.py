from sqlalchemy import create_engine, Column, Integer, String, ForeignKey,UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()
# Define the User model with relationships to other models
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    tasks = relationship("Task", backref="user")
# Define the Task model with relationships to other models
class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    subtasks = relationship("Subtask", backref="task")
# Define the Subtask model with relationships to other models
class Subtask(Base):
    __tablename__ = 'subtasks'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    task_id = Column(Integer, ForeignKey('tasks.id'))
    __table_args__ = (UniqueConstraint('task_id', 'title', name='unique_subtask'),)
# Create the engine that will interact with the database
engine = create_engine('sqlite:///todo.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

Session = sessionmaker(bind=engine)
session = Session()
# Functions to perform operations
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
def get_users():
    return session.query(User).all()

def get_tasks(user):
    return session.query(Task).filter_by(user=user).all()

def get_subtasks(task):
    return session.query(Subtask).filter_by(task=task).all()
# Main function to run the application  
def main():
    users = get_users()
    if not users:
        user = add_user("Default User")
    else:
        user = users[0]

    while True:
        print("1. Add task")
        print("2. View tasks")
        print("3. Change task")
        print("4. Delete task")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            title = input("Enter task title: ")
            task = add_task(title, user)
            print("Task added successfully!")

        elif choice == "2":
            tasks = get_tasks(user)
            if not tasks:
                print("No tasks available!")
            else:
                for i, task in enumerate(tasks, start=1):
                    print(f"{i}. {task.title}")
                    subtasks = get_subtasks(task)
                    for j, subtask in enumerate(subtasks, start=1):
                        print(f"  {j}. {subtask.title}")

        elif choice == "3":
            tasks = get_tasks(user)
            if not tasks:
                print("No tasks available to change!")
            else:
                for i, task in enumerate(tasks, start=1):
                    print(f"{i}. {task.title}")
                task_number = int(input("Enter the task number to change: "))
                if task_number > 0 and task_number <= len(tasks):
                    new_title = input("Enter the new task title: ")
                    task = tasks[task_number - 1]
                    task.title = new_title
                    session.commit()
                    print("Task changed successfully!")
                else:
                    print("Invalid task number!")

        elif choice == "4":
            tasks = get_tasks(user)
            if not tasks:
                print("No tasks available to delete!")
            else:
                for i, task in enumerate(tasks, start=1):
                    print(f"{i}. {task.title}")
                task_number = int(input("Enter the task number to delete: "))
                if task_number > 0 and task_number <= len(tasks):
                    task = tasks[task_number - 1]
                    session.delete(task)
                    session.commit()
                    print("Task deleted successfully!")
                else:
                    print("Invalid task number!")

        elif choice == "5":
            print("Exiting the application. Goodbye!")
            break

        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main()

    