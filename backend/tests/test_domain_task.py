import uuid
import pytest
from app.domain.entities import TaskEntity


def test_task_status_change():
    t = TaskEntity(id=uuid.uuid4(), tenant_id=uuid.uuid4(), project_id=uuid.uuid4(), title="A")
    assert t.status == "todo"
    t.change_status("in_progress")
    assert t.status == "in_progress"
    t.change_status("done")
    assert t.status == "done"


def test_task_status_invalid():
    t = TaskEntity(id=uuid.uuid4(), tenant_id=uuid.uuid4(), project_id=uuid.uuid4(), title="A")
    with pytest.raises(ValueError):
        t.change_status("invalid_status")
