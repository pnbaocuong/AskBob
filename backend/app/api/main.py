from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from .routes import auth, projects, tasks
from ..infrastructure.config import get_settings

app = FastAPI(title="AskBob AI PMS", version="0.1.0")

settings = get_settings()
origins = settings.allowed_origins
allow_credentials = False if origins == ["*"] else True
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Basic health endpoint."""
    return JSONResponse({"status": "ok"})


app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(projects.router, prefix="/projects", tags=["projects"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
