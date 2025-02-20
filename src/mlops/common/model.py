from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, TypeVar

from typing_extensions import Generic


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


IdType = TypeVar('IdType', int, None)


@dataclass
class TrainingTask(Generic[IdType]):
    id: IdType
    name: str
    input_dir: Path
    output_dir: Path
    config: dict[str, Any]
    created_at: datetime
    updated_at: datetime | None
