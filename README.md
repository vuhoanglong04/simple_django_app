# Simple Django Todo App

This is a minimal Django todo app configured to use PostgreSQL.

Postgres Docker command (starts the DB):

```bash
docker run --name todo-postgres -e POSTGRES_USER=todo_user -e POSTGRES_PASSWORD=todo_pass -e POSTGRES_DB=todo_db -p 5432:5432 -d postgres:15
```

Quick setup:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Notes:
- Database settings are in `mysite/settings.py`.
- The app lives in the `todo` package.
