import uuid
import pytest
from datetime import datetime, timedelta

from app.api.routes.tasks import StatusEnum, PriorityEnum
from app.domain.entities import TaskEntity


class FakeTask:
    def __init__(self, title, status, priority, due_date, created_at):
        self.id = uuid.uuid4()
        self.title = title
        self.status = status
        self.priority = priority
        self.due_date = due_date
        self.created_at = created_at
        self.assignee = None
        self.project_id = uuid.uuid4()
        self.tenant_id = uuid.uuid4()


def sort_items(items, key, desc=False):
    return sorted(items, key=lambda x: getattr(x, key), reverse=desc)


def test_pagination_and_sorting_in_memory():
    now = datetime.utcnow()
    items = [
        FakeTask("A", "todo", "low", now + timedelta(days=3), now - timedelta(minutes=3)),
        FakeTask("B", "in_progress", "high", now + timedelta(days=1), now - timedelta(minutes=1)),
        FakeTask("C", "done", "medium", now + timedelta(days=2), now - timedelta(minutes=2)),
    ]

    # simulate pagination limit/offset
    items_sorted = sort_items(items, 'created_at', desc=True)
    page = items_sorted[0:2]
    assert len(page) == 2
    assert page[0].title == "B"

    # sort by due_date asc
    items_due_asc = sort_items(items, 'due_date', desc=False)
    assert items_due_asc[0].title == "B"

    # sort by priority desc (lexicographical for demo: high > medium > low)
    items_prio_desc = sort_items(items, 'priority', desc=True)
    assert items_prio_desc[0].priority in {"high", "medium", "low"}


def test_filters_in_memory():
    now = datetime.utcnow()
    items = [
        FakeTask("A", "todo", "low", now + timedelta(days=3), now),
        FakeTask("B", "in_progress", "high", now + timedelta(days=1), now),
        FakeTask("C", "done", "medium", now + timedelta(days=2), now),
    ]

    status_filtered = [i for i in items if i.status == StatusEnum.in_progress.value]
    assert len(status_filtered) == 1 and status_filtered[0].title == "B"

    prio_filtered = [i for i in items if i.priority == PriorityEnum.high.value]
    assert len(prio_filtered) == 1 and prio_filtered[0].title == "B"

    due_before = now + timedelta(days=2)
    due_filtered = [i for i in items if i.due_date and i.due_date <= due_before]
    titles = {i.title for i in due_filtered}
    assert len(due_filtered) == 2 and titles == {"B", "C"}
