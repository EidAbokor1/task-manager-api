from sqlalchemy import select
from sqlalchemy.orm import Session

from database import engine
from models_practice import Task

def create_task(title: str):
    title = title.strip()
    if title == "":
        raise ValueError("Title cannot be empty")
    with Session(engine) as session:
        task = Task(title=title, completed=False)
        session.add(task)
        session.commit()
        return {
            "id": task.id,
            "title": task.title,
            "completed": task.completed,
        }

def list_tasks() -> list:
    with Session(engine) as session:
        statement = select(Task)
        db_tasks = session.scalars(statement).all()
        results = []
        for db_task in db_tasks:
            task_data = {
                        "id": db_task.id,
                        "title": db_task.title,
                        "completed": db_task.completed,
                        }
            results.append(task_data)
        return results

def get_task(task_id: int):
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if task is None:
            raise ValueError("Task not found")
        return{
            "id": task.id,
            "title": task.title,
            "completed": task.completed
        }

def complete_task(task_id: int):
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if task is None:
            raise ValueError("Task not found")
        task.completed = True
        session.commit()
        return {
            "id": task.id,
            "title": task.title,
            "completed": task.completed
        }

def delete_task(task_id: int):
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if  task is None:
            raise ValueError("Task not found")
        task_data = {
            "id": task.id,
            "title": task.title,
            "completed": task.completed,
        }
        session.delete(task)
        session.commit()
        return task_data
