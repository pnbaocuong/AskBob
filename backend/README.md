# Backend (FastAPI + SQLAlchemy 2.0 + Alembic)

Follows Clean Architecture: `domain`, `application`, `infrastructure`, `api`. Multi-tenancy is enforced via `tenant_id`. JWT is used for authentication.

## Structure
- `app/api`: routers, dependencies, main app
- `app/domain`: entities and business rules
- `app/application`: use cases, repository interfaces
- `app/infrastructure`: config, database (models, session), security, repository implementations
- `alembic`: migration scripts

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
cp backend/env.example backend/.env
```
Edit `DATABASE_URL` and `SYNC_DATABASE_URL` for PostgreSQL.

## Migrations
```bash
cd backend
alembic upgrade head
```

## Run server
```bash
uvicorn app.api.main:app --reload --app-dir backend --port 12000
```

## Docs
- Swagger: `http://localhost:12000/docs`

## Basic flow
1) `POST /auth/register` → get JWT
2) `POST /auth/login` → JWT
3) CRUD `/projects` and `/tasks` with header `Authorization: Bearer <token>`
