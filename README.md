# Task API

A REST API built with Python, FastAPI and PostgreSQL. Users register, log in,
and manage their own private tasks.

## Features
- Registration and login with JWT tokens and bcrypt password hashing
- Task CRUD with filtering and pagination
- Each user can only access their own tasks
- Database migrations with Alembic
- Automated tests with pytest

## Setup

You need Python 3.12+ and PostgreSQL installed.

1. Create the database (in `psql`, logged in as the admin user):
   ```sql
   CREATE USER taskuser WITH PASSWORD 'taskpass';
   CREATE DATABASE taskdb OWNER taskuser;
   ```
2. Install and configure:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env
   ```
   Then edit `.env` and set a real `SECRET_KEY`.
3. Create the tables and start the server:
   ```bash
   alembic upgrade head
   uvicorn app.main:app --reload
   ```
4. Open http://localhost:8000/docs

## Running the tests
```bash
pytest
```
Tests use an in-memory database, so your real data is never touched.

## Endpoints

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/auth/register` | No | Create an account |
| POST | `/api/v1/auth/login` | No | Get an access token |
| GET | `/api/v1/users/me` | Yes | Current user |
| POST | `/api/v1/tasks` | Yes | Create a task |
| GET | `/api/v1/tasks` | Yes | List tasks (`status`, `limit`, `offset`) |
| GET | `/api/v1/tasks/{id}` | Yes | Get one task |
| PATCH | `/api/v1/tasks/{id}` | Yes | Update a task |
| DELETE | `/api/v1/tasks/{id}` | Yes | Delete a task |

## Project layout
```
app/
  main.py          app setup and routing
  core/            settings and security helpers
  db/              database connection
  models/          database tables
  schemas/         request/response validation
  api/             dependencies and route handlers
alembic/           database migrations
tests/             automated tests
```

## Changing the database
Edit a model, then:
```bash
alembic revision --autogenerate -m "describe the change"
alembic upgrade head
```