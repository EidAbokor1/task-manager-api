# Task Management API

A Python backend learning project built incrementally from an in-memory task manager into a PostgreSQL-backed HTTP API.

The focus is understanding request flow, validation, persistence, transactions, migrations, and automated testing. This is a working educational project, not a production-hardened service.

## Implemented

- FastAPI endpoints for creating, listing, retrieving, completing, and deleting tasks.
- Pydantic request validation and application checks for empty or whitespace-only titles.
- SQLAlchemy ORM with Psycopg and PostgreSQL persistence.
- Alembic initial schema migration, verified against a separate empty database.
- Eight pytest tests covering successful operations and expected errors.
- A dedicated test database, database-name guard, and cleanup fixture.
- PostgreSQL running in Docker with a persistent named volume.

The API currently runs on the host. An API Dockerfile and Compose setup are still planned.

## Request flow

```text
HTTP client
    -> Uvicorn / FastAPI (api.py)
    -> task operations (task_manager.py)
    -> SQLAlchemy Session / Engine
    -> Psycopg
    -> PostgreSQL
```

## Project files

| File | Responsibility |
| --- | --- |
| `api.py` | HTTP routes, request model, and error responses |
| `task_manager.py` | Validation and database-backed task operations |
| `database.py` | Environment configuration and SQLAlchemy engine |
| `models_practice.py` | SQLAlchemy table mapping for `Task` |
| `alembic/` | Migration environment and version scripts |
| `tests/` | Validation and API integration tests |
| `requirements.txt` | Pinned direct runtime and migration dependencies |
| `requirements-dev.txt` | Runtime dependencies plus test tools |

Earlier learning scripts (`main.py`, `class_practice.py`, `db_practice.py`, and `sqlalchemy_practice.py`) are retained as exercises. Some create, modify, or delete records when run. The API entry point is `api:app`.

## Local setup

Prerequisites: Python 3.14 (the version used during development), Docker, and an available local port 5432. The commands below assume a Unix-like shell and are run from the repository directory.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

Set `TASK_DB_PASSWORD` in the terminal that will run the API, migrations, or tests. For example, in zsh, prompt without echoing the password:

```zsh
read -rs 'TASK_DB_PASSWORD?Database password: '
export TASK_DB_PASSWORD
```

Do not commit database credentials. Environment exports belong to the current shell and are inherited by its child processes.

### Start PostgreSQL

For a fresh local setup:

```bash
docker run -d \
  --name task-manager-db \
  -e POSTGRES_USER=task_user \
  -e POSTGRES_PASSWORD="$TASK_DB_PASSWORD" \
  -e POSTGRES_DB=task_manager \
  -p 127.0.0.1:5432:5432 \
  -v task_manager_pgdata:/var/lib/postgresql \
  postgres:18
```

Wait for PostgreSQL to be ready:

```bash
docker exec task-manager-db pg_isready -h 127.0.0.1 -U task_user -d task_manager
```

If that container already exists, use `docker start task-manager-db`. With an existing volume, use the password configured when the database was first initialized; changing the container environment does not reset it.

The volume retains database files across container replacement when reused. Deleting the volume deletes that stored database data.

### Apply migrations and run the API

```bash
python -m alembic upgrade head
python -m uvicorn api:app --reload
```

The initial migration creates the `tasks` table. An existing manually created table must be checked for schema compatibility before baselining it with Alembic; `stamp` only records a version and does not verify or create the schema.

Interactive API documentation: <http://127.0.0.1:8000/docs>.

Configuration in this first version:

| Setting | Value |
| --- | --- |
| PostgreSQL host | `127.0.0.1` |
| PostgreSQL port | `5432` |
| Database user | `task_user` |
| Database name | `TASK_DB_NAME`, default `task_manager` |
| Database password | Required `TASK_DB_PASSWORD` |

The fixed host is for a host-run API. It will need configuration changes when the API is containerized.

## API endpoints

| Method | Path | Successful response |
| --- | --- | --- |
| GET | `/tasks` | `200`, list of tasks |
| GET | `/tasks/{task_id}` | `200`, one task |
| POST | `/tasks` | `201`, created task |
| PATCH | `/tasks/{task_id}/complete` | `200`, completed task |
| DELETE | `/tasks/{task_id}` | `200`, deleted task |

Task creation example:

```bash
curl -i -X POST http://127.0.0.1:8000/tasks \
  -H 'Content-Type: application/json' \
  -d '{"title": "Learn backend engineering"}'

curl -i http://127.0.0.1:8000/tasks
```

Empty and whitespace-only titles return `400`; a missing required title returns `422`; a task ID that is not found returns `404`.

## Tests

Create a separate disposable database and apply the same migrations:

```bash
docker exec task-manager-db createdb -U task_user task_manager_test
TASK_DB_NAME=task_manager_test python -m alembic upgrade head
TASK_DB_NAME=task_manager_test python -m pytest tests -v
```

Create the test database only once; if it already exists, proceed to migrations. Uvicorn is not required: `TestClient` calls the application directly. PostgreSQL must be available for the database tests.

The suite refuses to run unless the engine targets `task_manager_test`. Tests requesting `clean_database` delete all task rows in that dedicated database before and after the test. Never use that database for data you want to keep.

Tests use database-generated IDs rather than assuming a sequence starts at 1. The cleanup fixture does not reset the ID sequence.

At this checkpoint, all eight tests pass. Starlette 1.6.0 with the installed AnyIO version emits a `BlockingPortal` deprecation warning; this is a dependency warning rather than a failed test. The requirements pin direct dependencies, not every transitive dependency.

## Next steps

- Package the API with a Dockerfile and Compose configuration.
- Improve configuration and operational reliability as the project grows.
- Add authentication, background processing, and AI/MCP features after the foundation is understood.

Authentication, deployment infrastructure, and AI functionality are not implemented in this checkpoint.
