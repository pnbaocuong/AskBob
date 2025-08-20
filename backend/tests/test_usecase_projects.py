import uuid
import asyncio
import pytest

from app.application.use_cases.projects import list_projects_for_tenant, create_project
from app.domain.entities import ProjectEntity


class FakeProjectRepo:
    def __init__(self):
        self.items = []

    async def list_by_tenant(self, tenant_id):
        return [i for i in self.items if i.tenant_id == tenant_id]

    async def create(self, tenant_id, name, description):
        p = ProjectEntity(id=uuid.uuid4(), tenant_id=tenant_id, name=name, description=description)
        self.items.append(p)
        return p


@pytest.mark.asyncio
async def test_project_usecases_create_and_list():
    repo = FakeProjectRepo()
    t1 = uuid.uuid4()
    t2 = uuid.uuid4()

    await create_project(repo, t1, 'P1', None)
    await create_project(repo, t2, 'P2', None)

    list1 = await list_projects_for_tenant(repo, t1)
    assert len(list1) == 1 and list1[0].name == 'P1'

    list2 = await list_projects_for_tenant(repo, t2)
    assert len(list2) == 1 and list2[0].name == 'P2'
