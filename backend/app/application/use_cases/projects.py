"""Project use cases.

Contains orchestration logic that is independent from frameworks and
infrastructure so it can be unit tested easily.
"""

import uuid
from typing import Optional, Sequence

from ..repositories import IProjectRepository
from ...domain.entities import ProjectEntity


async def list_projects_for_tenant(repo: IProjectRepository, tenant_id: uuid.UUID) -> Sequence[ProjectEntity]:
    """List projects for the given tenant."""
    return await repo.list_by_tenant(tenant_id)


async def create_project(repo: IProjectRepository, tenant_id: uuid.UUID, name: str, description: Optional[str]) -> ProjectEntity:
    """Create a project under the given tenant and return the domain entity."""
    return await repo.create(tenant_id, name, description)
