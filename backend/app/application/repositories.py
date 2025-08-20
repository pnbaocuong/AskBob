from __future__ import annotations
from typing import Protocol, Sequence, Optional
import uuid

from ..domain.entities import ProjectEntity, TaskEntity


class IProjectRepository(Protocol):
    async def list_by_tenant(self, tenant_id: uuid.UUID) -> Sequence[ProjectEntity]:
        ...

    async def create(self, tenant_id: uuid.UUID, name: str, description: Optional[str]) -> ProjectEntity:
        ...


class ITaskRepository(Protocol):
    async def list_by_tenant(self, tenant_id: uuid.UUID, project_id: Optional[uuid.UUID] = None) -> Sequence[TaskEntity]:
        ...

    async def create(self, tenant_id: uuid.UUID, project_id: uuid.UUID, title: str, status: str, assignee: Optional[str]) -> TaskEntity:
        ...
