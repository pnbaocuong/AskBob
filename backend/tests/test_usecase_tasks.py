import uuid
import pytest

from app.application.use_cases.tasks import list_tasks_for_tenant, create_task
from app.domain.entities import TaskEntity


class FakeTaskRepo:
    def __init__(self):
        self.items = []

    async def list_by_tenant(self, tenant_id, project_id=None):
        res = [i for i in self.items if i.tenant_id == tenant_id]
        if project_id:
            res = [i for i in res if i.project_id == project_id]
        return res

    async def create(self, tenant_id, project_id, title, status, assignee):
        t = TaskEntity(id=uuid.uuid4(), tenant_id=tenant_id, project_id=project_id, title=title, status=status, assignee=assignee)
        self.items.append(t)
        return t


@pytest.mark.asyncio
async def test_task_usecases_create_and_list():
    repo = FakeTaskRepo()
    t1 = uuid.uuid4()
    p1 = uuid.uuid4()

    await create_task(repo, t1, p1, 'T1', 'todo', None)
    await create_task(repo, t1, p1, 'T2', 'in_progress', 'alice')

    all_tasks = await list_tasks_for_tenant(repo, t1)
    assert len(all_tasks) == 2

    by_project = await list_tasks_for_tenant(repo, t1, p1)
    assert len(by_project) == 2
    assert any(x.assignee == 'alice' for x in by_project)
