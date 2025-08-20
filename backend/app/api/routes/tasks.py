"""Task endpoints with tenant isolation and basic CRUD."""

import uuid
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from enum import Enum
from datetime import datetime

from ..dependencies import get_db_session, get_current_tenant_id
from ...infrastructure.db.models import Task, Project
from ...infrastructure.config import get_settings

router = APIRouter()
settings = get_settings()


class StatusEnum(str, Enum):
    """Allowed task statuses."""
    todo = "todo"
    in_progress = "in_progress"
    done = "done"

class PriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TaskCreate(BaseModel):
    """Payload to create a task under a project."""
    title: str
    status: StatusEnum = StatusEnum.todo
    assignee: Optional[str] = None
    priority: PriorityEnum = PriorityEnum.medium
    due_date: Optional[datetime] = None
    project_id: uuid.UUID


class TaskUpdate(BaseModel):
    """Payload to update a task fields."""
    title: Optional[str] = None
    status: Optional[StatusEnum] = None
    assignee: Optional[str] = None
    priority: Optional[PriorityEnum] = None
    due_date: Optional[datetime] = None


class TaskOut(BaseModel):
    """Task response model."""
    id: uuid.UUID
    title: str
    status: str
    assignee: Optional[str] = None
    priority: str
    due_date: Optional[datetime] = None
    project_id: uuid.UUID

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    total: int
    items: list[TaskOut]


@router.get("/", response_model=TaskListResponse)
async def list_tasks(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    tenant_id: Annotated[uuid.UUID, Depends(get_current_tenant_id)],
    project_id: Optional[uuid.UUID] = None,
    limit: int = Query(settings.default_page_size, ge=1, le=settings.max_page_size),
    offset: int = Query(0, ge=0),
    status_filter: Optional[StatusEnum] = None,
    priority_filter: Optional[PriorityEnum] = None,
    due_before: Optional[datetime] = None,
    due_after: Optional[datetime] = None,
    sort: Optional[str] = Query(None, description="Sort by: created_at|due_date|priority (prefix - for desc)"),
):
    """List tasks for current tenant; filter/sort/pagination supported."""
    base = select(Task).where(Task.tenant_id == tenant_id)
    if project_id:
        base = base.where(Task.project_id == project_id)
    if status_filter:
        base = base.where(Task.status == status_filter.value)
    if priority_filter:
        base = base.where(Task.priority == priority_filter.value)
    if due_before:
        base = base.where(Task.due_date != None).where(Task.due_date <= due_before)  # noqa: E711
    if due_after:
        base = base.where(Task.due_date != None).where(Task.due_date >= due_after)  # noqa: E711

    # total
    total_result = await session.execute(base)
    total = len(total_result.scalars().all())

    # sort
    order = Task.created_at.desc()
    if sort:
        s = sort.strip().lower()
        desc = s.startswith('-')
        key = s[1:] if desc else s
        if key == 'created_at':
            order = Task.created_at.desc() if desc else Task.created_at.asc()
        elif key == 'due_date':
            order = Task.due_date.desc() if desc else Task.due_date.asc()
        elif key == 'priority':
            order = Task.priority.desc() if desc else Task.priority.asc()

    page_q = base.order_by(order).limit(limit).offset(offset)
    result = await session.execute(page_q)
    items = [TaskOut.model_validate(t) for t in result.scalars().all()]
    return TaskListResponse(total=total, items=items)


@router.post("/", response_model=TaskOut, status_code=201)
async def create_task(
    body: TaskCreate,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    tenant_id: Annotated[uuid.UUID, Depends(get_current_tenant_id)],
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
        priority=body.priority.value,
        due_date=body.due_date,
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
    tenant_id: Annotated[uuid.UUID, Depends(get_current_tenant_id)],
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
    if body.priority is not None:
        task.priority = body.priority.value
    if body.due_date is not None:
        task.due_date = body.due_date

    await session.commit()
    await session.refresh(task)
    return TaskOut.model_validate(task)


@router.delete("/{task_id}", status_code=204)
async def delete_task(
    task_id: uuid.UUID,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    tenant_id: Annotated[uuid.UUID, Depends(get_current_tenant_id)],
):
    """Delete a task owned by current tenant."""
    result = await session.execute(select(Task).where(Task.id == task_id, Task.tenant_id == tenant_id))
    task = result.scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    await session.delete(task)
    await session.commit()
    return None
