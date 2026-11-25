import os
from sqlalchemy import URL, create_engine

password = os.environ["TASK_DB_PASSWORD"]

database_url = URL.create(
    "postgresql+psycopg",
    username="task_user",
    password=password,
    host="127.0.0.1",
    port=5432,
    database=os.environ.get("TASK_DB_NAME", "task_manager")
)

engine = create_engine(database_url, echo=True)