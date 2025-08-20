"""Task endpoints with tenant isolation and basic CRUD."""

import uuid
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from enum import Enum

from ..dependencies import get_db_session, get_current_tenant_id
from ...infrastructure.db.models import Task, Project

router = APIRouter()


class StatusEnum(str, Enum):
    """Allowed task statuses."""
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class TaskCreate(BaseModel):
    """Payload to create a task under a project."""
    title: str
    status: StatusEnum = StatusEnum.todo
    assignee: Optional[str] = None
    project_id: uuid.UUID


class TaskUpdate(BaseModel):
    """Payload to update a task fields."""
    title: Optional[str] = None
    status: Optional[StatusEnum] = None
    assignee: Optional[str] = None


class TaskOut(BaseModel):
    """Task response model."""
    id: uuid.UUID
    title: str
    status: str
    assignee: Optional[str] = None
    project_id: uuid.UUID

    class Config:
        from_attributes = True


@router.get("/", response_model=list[TaskOut])
async def list_tasks(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    tenant_id: Annotated[str, Depends(get_current_tenant_id)],
    project_id: Optional[uuid.UUID] = None,
):
    """List tasks for current tenant; optionally filter by project."""
    query = select(Task).where(Task.tenant_id == tenant_id)
    if project_id:
        query = query.where(Task.project_id == project_id)
    result = await session.execute(query.order_by(Task.created_at.desc()))
    tasks = result.scalars().all()
    return [TaskOut.model_validate(t) for t in tasks]


@router.post("/", response_model=TaskOut, status_code=201)
async def create_task(
    body: TaskCreate,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    tenant_id: Annotated[str, Depends(get_current_tenant_id)],
):
    """Create a task under a project owned by current tenant."""
    # Validate project belongs to tenant
    p = await session.execute(select(Project).where(Project.id == body.project_id, Project.tenant_id == tenant_id))
    if p.scalar_one_or_none() is None:
        raise HTTPException(status_code=404, detail="Project not found")

    task = Task(
        title=body.title,
        status=body.status.value,
        assignee=body.assignee,
        project_id=body.project_id,
        tenant_id=tenant_id,
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return TaskOut.model_validate(task)


@router.put("/{task_id}", response_model=TaskOut)
async def update_task(
    task_id: uuid.UUID,
    body: TaskUpdate,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    tenant_id: Annotated[str, Depends(get_current_tenant_id)],
):
    """Update a task owned by current tenant."""
    result = await session.execute(select(Task).where(Task.id == task_id, Task.tenant_id == tenant_id))
    task = result.scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    if body.title is not None:
        task.title = body.title
    if body.status is not None:
        task.status = body.status.value
    if body.assignee is not None:
        task.assignee = body.assignee

    await session.commit()
    await session.refresh(task)
    return TaskOut.model_validate(task)


@router.delete("/{task_id}", status_code=204)
async def delete_task(
    task_id: uuid.UUID,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    tenant_id: Annotated[str, Depends(get_current_tenant_id)],
):
    """Delete a task owned by current tenant."""
    result = await session.execute(select(Task).where(Task.id == task_id, Task.tenant_id == tenant_id))
    task = result.scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    await session.delete(task)
    await session.commit()
    return None
