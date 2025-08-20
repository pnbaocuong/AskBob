import uuid
from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...application.repositories import IProjectRepository, ITaskRepository
from ..db.models import Project, Task
from ...domain.entities import ProjectEntity, TaskEntity


class ProjectRepositorySQLAlchemy(IProjectRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_by_tenant(self, tenant_id: uuid.UUID) -> Sequence[ProjectEntity]:
        result = await self._session.execute(select(Project).where(Project.tenant_id == tenant_id).order_by(Project.created_at.desc()))
        rows = result.scalars().all()
        return [ProjectEntity(id=p.id, tenant_id=p.tenant_id, name=p.name, description=p.description, created_at=p.created_at) for p in rows]

    async def create(self, tenant_id: uuid.UUID, name: str, description: Optional[str]) -> ProjectEntity:
        project = Project(name=name, description=description, tenant_id=tenant_id)
        self._session.add(project)
        await self._session.commit()
        await self._session.refresh(project)
        return ProjectEntity(id=project.id, tenant_id=project.tenant_id, name=project.name, description=project.description, created_at=project.created_at)


class TaskRepositorySQLAlchemy(ITaskRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_by_tenant(self, tenant_id: uuid.UUID, project_id: Optional[uuid.UUID] = None) -> Sequence[TaskEntity]:
        query = select(Task).where(Task.tenant_id == tenant_id)
        if project_id:
            query = query.where(Task.project_id == project_id)
        result = await self._session.execute(query.order_by(Task.created_at.desc()))
        rows = result.scalars().all()
        return [TaskEntity(id=t.id, tenant_id=t.tenant_id, project_id=t.project_id, title=t.title, status=t.status, assignee=t.assignee, created_at=t.created_at) for t in rows]

    async def create(self, tenant_id: uuid.UUID, project_id: uuid.UUID, title: str, status: str, assignee: Optional[str]) -> TaskEntity:
        task = Task(tenant_id=tenant_id, project_id=project_id, title=title, status=status, assignee=assignee)
        self._session.add(task)
        await self._session.commit()
        await self._session.refresh(task)
        return TaskEntity(id=task.id, tenant_id=task.tenant_id, project_id=task.project_id, title=task.title, status=task.status, assignee=task.assignee, created_at=task.created_at)
