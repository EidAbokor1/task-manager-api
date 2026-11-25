"""Direct Psycopg exercise; running it inserts a database row."""

import psycopg
from getpass import getpass

password = getpass("Database password: ")

with psycopg.connect(
    host="127.0.0.1",
    port=5432,
    dbname="task_manager",
    user="task_user",
    password=password,
    connect_timeout=5,
) as connection:
    print("Connected to PostgresSQL")
    title = "Learn Psycopg"
    result = connection.execute("""
    INSERT INTO tasks (title)
    VALUES (%s)
    RETURNING id, title, completed;
    """,
    (title,),
    )
    created_task = result.fetchone()
    print(created_task)
