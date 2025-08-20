import uuid
from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...application.repositories import IProjectRepository, ITaskRepository
from ..db.models import Project, Task
from ...domain.entities import ProjectEntity, TaskEntity


class ProjectRepositorySQLAlchemy(IProjectRepository):
    """Repository implementation for Projects using SQLAlchemy.

    Encapsulates data access so application/use-cases do not depend on
    SQLAlchemy directly (dependency inversion). This makes the business
    logic testable and keeps infrastructure behind an interface.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_by_tenant(self, tenant_id: uuid.UUID) -> Sequence[ProjectEntity]:
        """Return projects for a tenant ordered by creation date (desc)."""
        result = await self._session.execute(
            select(Project).where(Project.tenant_id == tenant_id).order_by(Project.created_at.desc())
        )
        rows = result.scalars().all()
        return [
            ProjectEntity(
                id=p.id, tenant_id=p.tenant_id, name=p.name, description=p.description, created_at=p.created_at
            )
            for p in rows
        ]

    async def create(self, tenant_id: uuid.UUID, name: str, description: Optional[str]) -> ProjectEntity:
        """Create a new project for the given tenant and return its domain entity."""
        project = Project(name=name, description=description, tenant_id=tenant_id)
        self._session.add(project)
        await self._session.commit()
        await self._session.refresh(project)
        return ProjectEntity(
            id=project.id,
            tenant_id=project.tenant_id,
            name=project.name,
            description=project.description,
            created_at=project.created_at,
        )


class TaskRepositorySQLAlchemy(ITaskRepository):
    """Repository implementation for Tasks using SQLAlchemy.

    Ensures every query is scoped by tenant to maintain strict isolation.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_by_tenant(self, tenant_id: uuid.UUID, project_id: Optional[uuid.UUID] = None) -> Sequence[TaskEntity]:
        """Return tasks in a tenant, optionally filtered by a project."""
        query = select(Task).where(Task.tenant_id == tenant_id)
        if project_id:
            query = query.where(Task.project_id == project_id)
        result = await self._session.execute(query.order_by(Task.created_at.desc()))
        rows = result.scalars().all()
        return [
            TaskEntity(
                id=t.id,
                tenant_id=t.tenant_id,
                project_id=t.project_id,
                title=t.title,
                status=t.status,
                assignee=t.assignee,
                created_at=t.created_at,
            )
            for t in rows
        ]

    async def create(
        self,
        tenant_id: uuid.UUID,
        project_id: uuid.UUID,
        title: str,
        status: str,
        assignee: Optional[str],
    ) -> TaskEntity:
        """Create a new task under a project for a tenant and return its domain entity."""
        task = Task(tenant_id=tenant_id, project_id=project_id, title=title, status=status, assignee=assignee)
        self._session.add(task)
        await self._session.commit()
        await self._session.refresh(task)
        return TaskEntity(
            id=task.id,
            tenant_id=task.tenant_id,
            project_id=task.project_id,
            title=task.title,
            status=task.status,
            assignee=task.assignee,
            created_at=task.created_at,
        )
