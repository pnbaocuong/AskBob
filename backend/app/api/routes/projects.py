"""Project endpoints with strict tenant isolation."""

import uuid
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..dependencies import get_db_session, get_current_tenant_id
from ...infrastructure.repositories.sqlalchemy_repositories import ProjectRepositorySQLAlchemy
from ...application.use_cases import projects as project_uc
from ...infrastructure.config import get_settings

router = APIRouter()
settings = get_settings()


class ProjectCreate(BaseModel):
    """Payload to create a project."""
    name: str
    description: Optional[str] = None


class ProjectUpdate(BaseModel):
    """Payload to update a project."""
    name: Optional[str] = None
    description: Optional[str] = None


class ProjectOut(BaseModel):
    """Project response model."""
    id: uuid.UUID
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class ProjectListResponse(BaseModel):
    total: int
    items: list[ProjectOut]


@router.get("/", response_model=ProjectListResponse)
async def list_projects(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    tenant_id: Annotated[uuid.UUID, Depends(get_current_tenant_id)],
    limit: int = Query(settings.default_page_size, ge=1, le=settings.max_page_size),
    offset: int = Query(0, ge=0),
):
    """List projects for current tenant with simple pagination."""
    # Fetch total
    from ...infrastructure.db.models import Project
    total_result = await session.execute(select(Project).where(Project.tenant_id == tenant_id))
    total = len(total_result.scalars().all())

    # Fetch page
    repo = ProjectRepositorySQLAlchemy(session)
    # Use direct query here for pagination; repo could be extended to support pagination if needed
    result = await session.execute(
        select(Project)
        .where(Project.tenant_id == tenant_id)
        .order_by(Project.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    projects = result.scalars().all()
    items = [ProjectOut.model_validate(p) for p in projects]
    return ProjectListResponse(total=total, items=items)


@router.post("/", response_model=ProjectOut, status_code=201)
async def create_project(
    body: ProjectCreate,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    tenant_id: Annotated[uuid.UUID, Depends(get_current_tenant_id)],
):
    """Create a project for current tenant."""
    repo = ProjectRepositorySQLAlchemy(session)
    created = await project_uc.create_project(repo, tenant_id, body.name, body.description)
    return ProjectOut(id=created.id, name=created.name, description=created.description)


@router.put("/{project_id}", response_model=ProjectOut)
async def update_project(
    project_id: uuid.UUID,
    body: ProjectUpdate,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    tenant_id: Annotated[uuid.UUID, Depends(get_current_tenant_id)],
):
    """Update a project owned by current tenant."""
    from ...infrastructure.db.models import Project

    result = await session.execute(select(Project).where(Project.id == project_id, Project.tenant_id == tenant_id))
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
    tenant_id: Annotated[uuid.UUID, Depends(get_current_tenant_id)],
):
    """Delete a project owned by current tenant."""
    from ...infrastructure.db.models import Project

    result = await session.execute(select(Project).where(Project.id == project_id, Project.tenant_id == tenant_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    await session.delete(project)
    await session.commit()
    return None
