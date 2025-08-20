from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class ProjectEntity:
    id: uuid.UUID
    tenant_id: uuid.UUID
    name: str
    description: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)


ALLOWED_STATUSES = {"todo", "in_progress", "done"}


@dataclass
class TaskEntity:
    id: uuid.UUID
    tenant_id: uuid.UUID
    project_id: uuid.UUID
    title: str
    status: str = "todo"
    assignee: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)

    def change_status(self, new_status: str) -> None:
        if new_status not in ALLOWED_STATUSES:
            raise ValueError("Invalid status")
        self.status = new_status
