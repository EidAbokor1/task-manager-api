from getpass import getpass
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import Session
from models_practice import Task

password = getpass("Database password: ")

database_url = URL.create(
    "postgresql+psycopg",
    username="task_user",
    password=password,
    host="127.0.0.1",
    port=5432,
    database="task_manager",
)

engine = create_engine(database_url, echo=True)
with Session(engine) as session:
    new_task = Task(title="Learn SQLAlchemy", completed=False)
    session.add(new_task)
    session.commit()
    print("Created:", new_task.id, new_task.title)
