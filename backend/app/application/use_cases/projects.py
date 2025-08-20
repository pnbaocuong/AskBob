import uuid
from typing import Optional, Sequence

from ..repositories import IProjectRepository
from ...domain.entities import ProjectEntity


async def list_projects_for_tenant(repo: IProjectRepository, tenant_id: uuid.UUID) -> Sequence[ProjectEntity]:
    return await repo.list_by_tenant(tenant_id)


async def create_project(repo: IProjectRepository, tenant_id: uuid.UUID, name: str, description: Optional[str]) -> ProjectEntity:
    return await repo.create(tenant_id, name, description)
