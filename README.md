# Task Management API

I'm building this to get more comfortable writing Python and understanding what happens behind an API request. It started with a list of dictionaries and now stores tasks in PostgreSQL.

You can create, list, find, complete and delete tasks. It has input validation, error responses, Alembic migrations and eight passing tests using a separate test database.

Built with Python, FastAPI, Pydantic, SQLAlchemy and Psycopg. PostgreSQL runs in Docker; the API currently runs locally. Packaging the API in Docker is next.

## How it fits together

`api.py` handles HTTP requests, `task_manager.py` contains the task operations, `models.py` maps tasks to database rows, and `database.py` sets up the engine.

Earlier learning scripts live in `practice/`. Run them from the project root as modules, for example `python -m practice.class_practice`. The database exercises change records when run. Start the API with `api:app`.

## Run locally

You'll need Docker and Python. I built and tested this with Python 3.14. Run these commands from the project folder.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

Set a local database password. In zsh, this prompts without displaying it:

```zsh
read -rs 'TASK_DB_PASSWORD?Database password: '
export TASK_DB_PASSWORD
```

For a fresh database:

```bash
docker run -d --name task-manager-db \
  -e POSTGRES_USER=task_user \
  -e POSTGRES_PASSWORD="$TASK_DB_PASSWORD" \
  -e POSTGRES_DB=task_manager \
  -p 127.0.0.1:5432:5432 \
  -v task_manager_pgdata:/var/lib/postgresql \
  postgres:18

docker exec task-manager-db pg_isready -U task_user -d task_manager
```

Once PostgreSQL is accepting connections:

```bash
python -m alembic upgrade head
python -m uvicorn api:app --reload
```

Open [localhost:8000/docs](http://127.0.0.1:8000/docs) to try the endpoints.

If the container already exists, use `docker start task-manager-db` and the password used when it was first created. Keep `TASK_DB_PASSWORD` set in the terminal running the app or migrations. The named volume keeps the data across container replacement; deleting it removes that data.

The database name defaults to `task_manager` and can be changed with `TASK_DB_NAME`. The host, port and user are currently fixed in `database.py`. The migration commands above assume a fresh database or one already managed by these migrations.

## Endpoints

```text
GET    /tasks
GET    /tasks/{task_id}
POST   /tasks
PATCH  /tasks/{task_id}/complete
DELETE /tasks/{task_id}
```

Example request:

```bash
curl -i -X POST http://127.0.0.1:8000/tasks \
  -H 'Content-Type: application/json' \
  -d '{"title": "Learn backend engineering"}'
```

Creation returns `201`. Empty titles return `400`, a missing title returns `422`, and missing tasks return `404`.

## Tests

Create the test database once, then migrate it and run the suite:

```bash
docker exec task-manager-db createdb -U task_user task_manager_test
TASK_DB_NAME=task_manager_test python -m alembic upgrade head
TASK_DB_NAME=task_manager_test python -m pytest tests -v
```

PostgreSQL needs to be running; Uvicorn doesn't. The tests check validation, CRUD and missing-task responses. A guard requires the test database name, and the cleanup fixture deletes its task rows before and after each database test.

All eight tests pass. There's one remaining Starlette/AnyIO deprecation warning. Dependencies are listed in `requirements.txt` and `requirements-dev.txt`; direct versions are pinned, transitive versions aren't locked.

Next: Docker packaging and Compose. Authentication, background jobs and AI/MCP features will come later.
