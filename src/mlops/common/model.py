from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class TrainingStatus:
    name: str
    phase: str
    progress: float
    description: str
    is_complete: bool


@dataclass
class WorkerStatus:
    id: str
    task_type: str
    version: str
    healthy: bool
    has_task: bool
    joined_at: datetime | None
    created_at: datetime


@dataclass
class WorkerData:
    host: str
    port: int
    task_type: str
    version: str
    options: dict[str, Any]
