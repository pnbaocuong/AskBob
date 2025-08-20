import uuid
from typing import Optional, Sequence

from ..repositories import ITaskRepository
from ...domain.entities import TaskEntity


async def list_tasks_for_tenant(repo: ITaskRepository, tenant_id: uuid.UUID, project_id: Optional[uuid.UUID] = None) -> Sequence[TaskEntity]:
    return await repo.list_by_tenant(tenant_id, project_id)


async def create_task(repo: ITaskRepository, tenant_id: uuid.UUID, project_id: uuid.UUID, title: str, status: str, assignee: Optional[str]) -> TaskEntity:
    return await repo.create(tenant_id, project_id, title, status, assignee)
