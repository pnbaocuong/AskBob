# AskBob AI Multi-tenant Project Management System

A Clean Architecture implementation with Backend (FastAPI + SQLAlchemy 2.0 + Alembic + PostgreSQL) and Frontend (React + Vite). Supports multi-tenancy via `tenant_id`, JWT authentication, CRUD for Projects/Tasks, and sample migrations.

## Requirements
- Python 3.11+
- Node.js 20+
- PostgreSQL 16+

## Backend Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
cp backend/env.example backend/.env
# edit backend/.env to point to your DB
```
Create the database (e.g., `askbobai`) referenced by `DATABASE_URL`.

Run Alembic migrations:
```bash
cd backend
alembic upgrade head
```

Run the server:
```bash
uvicorn app.api.main:app --reload --app-dir backend --port 12000
```
Swagger Docs: `http://localhost:12000/docs`

## Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
App: `http://localhost:12173`

## Docker Compose
```bash
docker compose up --build
```
- Backend: `http://localhost:12000` (Docs: `/docs`)
- Frontend: `http://localhost:12173`
- PostgreSQL: `localhost:12543`

## Testing
```bash
cd backend
pytest -q
```

## Quick Usage Flow
1) Register: POST `/auth/register` (the Login page already supports it), receive a token and store it in LocalStorage.
2) Login: POST `/auth/login`.
3) Projects: GET/POST/PUT/DELETE `/projects/`.
4) Tasks: GET/POST/PUT/DELETE `/tasks/`.

## Architecture
- Backend: `backend/app/` contains `domain`, `application`, `infrastructure`, `api` layers.
- Frontend: `frontend/src/` contains `component/`, `features/`, `lib/`, `routes/`.
- Multi-tenancy: all queries are filtered by the user `tenant_id` from JWT.

## Notes
- Env examples: `backend/env.example`, `frontend/.env.example`.
- Sample migration: `backend/alembic/versions/0001_initial.py`.
- Do not commit secrets (SECRET_KEY, DB credentials).
