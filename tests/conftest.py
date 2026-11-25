import pytest
from database import engine
from sqlalchemy import delete
from models_practice import Task

if engine.url.database != "task_manager_test":
    raise pytest.UsageError(
        "Run tests with TASK_DB_NAME=task_manager_test"
    )

@pytest.fixture
def clean_database():
    with engine.begin() as connection:
        connection.execute(delete(Task))

    yield

    with engine.begin() as connection:
        connection.execute(delete(Task))