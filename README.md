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

## Design decisions
- Clean Architecture: domain/use-cases are framework-agnostic for testability and maintainability; infrastructure behind interfaces (repositories) to enable easy swapping.
- Async SQLAlchemy: better concurrency characteristics for IO-bound API with DB pool tuning via env.
- tenant_id per-row isolation: simple, scalable, and index-friendly isolation pattern; works well with a single DB and aligns with product scope.
- Declarative migrations (Alembic): reproducible schema with clear upgrade/downgrade history.
- Containerized runtime: Nginx to serve static FE, Uvicorn for API; easy to scale and deploy.

## Assumptions
- Each user belongs to exactly one tenant; cross-tenant access is not allowed.
- Authorization is scoped to tenant-level; no advanced RBAC/roles beyond tenant isolation.
- Error handling is standardized at the API boundary; messages are concise and non-leaking.
- Pagination defaults: `DEFAULT_PAGE_SIZE=20`, `MAX_PAGE_SIZE=100`.
- Security: JWT HS256 for simplicity; deployments should terminate TLS via reverse proxy and rotate `SECRET_KEY` properly.

## Notes
- Env examples: `backend/env.example`, `frontend/.env.example`.
- Sample migration: `backend/alembic/versions/0001_initial.py` (and `0002_add_task_priority_due_date.py`).
- Do not commit secrets (SECRET_KEY, DB credentials).
