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
    """
    Training task data class.

    A Training task has its own base directory and input/output directory.

    Normally, the input/output directory is inside the base directory.

    .. code::

        base
        ├── input
        └── output


    But, the input directory can be outside the base directory for reusing the input data.
    In this case, the input directory should be linked to the base directory.

    For example:

    .. code::

        teamspace
            ├── tasks
            │   ├──base
            │      ├──input -> teamspace/datasets/input
            │      └── output
            └── datasets
                └── input
    """

    id: IdType
    """
    Incremental ID of the task.
    """

    name: str
    """
    Name of the task.
    """

    base_dir: Path
    """
    Base directory of the task.
    """

    input_dir: Path
    """
    Input directory of the task. Can be outside the base directory.
    
    If the input directory is outside the base directory, the input directory should be linked to the base directory.
    """

    task_type: str
    """
    An identifier of the task type. Indicates what worker should be used.
    """

    version: str
    """
    Worker version.
    """

    config: dict[str, Any]
    """
    Configuration of the task.
    """

    created_at: datetime
    """
    Created time of the task.
    """

    updated_at: datetime | None
    """
    Updated time of the task.
    """
