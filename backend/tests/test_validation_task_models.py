import uuid
import pytest
from datetime import datetime

from app.api.routes.tasks import TaskCreate, TaskUpdate, StatusEnum, PriorityEnum
from pydantic import ValidationError


def test_task_create_valid_enums():
    payload = TaskCreate(
        title="T",
        status=StatusEnum.in_progress,
        assignee="a",
        priority=PriorityEnum.high,
        due_date=datetime.utcnow(),
        project_id=uuid.uuid4(),
    )
    assert payload.status == StatusEnum.in_progress
    assert payload.priority == PriorityEnum.high


def test_task_create_invalid_status():
    with pytest.raises(ValidationError):
        TaskCreate(
            title="T",
            status="invalid",  # type: ignore
            project_id=uuid.uuid4(),
        )


def test_task_update_optional_fields():
    u = TaskUpdate(status=StatusEnum.done, assignee=None)
    assert u.status == StatusEnum.done
    assert u.assignee is None
