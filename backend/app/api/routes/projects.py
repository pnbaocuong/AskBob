import uuid
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_db_session, get_current_tenant_id
from ...infrastructure.repositories.sqlalchemy_repositories import ProjectRepositorySQLAlchemy
from ...application.use_cases import projects as project_uc

router = APIRouter()


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class ProjectOut(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


@router.get("/", response_model=list[ProjectOut])
async def list_projects(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    tenant_id: Annotated[str, Depends(get_current_tenant_id)],
):
    repo = ProjectRepositorySQLAlchemy(session)
    items = await project_uc.list_projects_for_tenant(repo, uuid.UUID(tenant_id))
    return [ProjectOut(id=i.id, name=i.name, description=i.description) for i in items]


@router.post("/", response_model=ProjectOut, status_code=201)
async def create_project(
    body: ProjectCreate,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    tenant_id: Annotated[str, Depends(get_current_tenant_id)],
):
    repo = ProjectRepositorySQLAlchemy(session)
    created = await project_uc.create_project(repo, uuid.UUID(tenant_id), body.name, body.description)
    return ProjectOut(id=created.id, name=created.name, description=created.description)


@router.put("/{project_id}", response_model=ProjectOut)
async def update_project(
    project_id: uuid.UUID,
    body: ProjectUpdate,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    tenant_id: Annotated[str, Depends(get_current_tenant_id)],
):
    # Temporarily keep direct update here for simplicity (can be moved to a dedicated use case later)
    from sqlalchemy import select
    from ...infrastructure.db.models import Project

    result = await session.execute(select(Project).where(Project.id == project_id, Project.tenant_id == uuid.UUID(tenant_id)))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if body.name is not None:
        project.name = body.name
    if body.description is not None:
        project.description = body.description

    await session.commit()
    await session.refresh(project)
    return ProjectOut.model_validate(project)


@router.delete("/{project_id}", status_code=204)
async def delete_project(
    project_id: uuid.UUID,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    tenant_id: Annotated[str, Depends(get_current_tenant_id)],
):
    from sqlalchemy import select
    from ...infrastructure.db.models import Project

    result = await session.execute(select(Project).where(Project.id == project_id, Project.tenant_id == uuid.UUID(tenant_id)))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    await session.delete(project)
    await session.commit()
    return None
