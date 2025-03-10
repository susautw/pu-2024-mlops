from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

@dataclass
class TrainingStatus:
    """
    Represents the status of a training task, tracking both its current (active) state and its historical states.

    This class encapsulates the details of a training task's progress. A task may have several historical
    status records along with one active status record. When determining the overall status of a task, follow this procedure:

    1. Retrieve the most recent historical status.
    2. If the most recent historical status is incomplete, consider the active status as the current state.

    The active status reflects the task's live state and is converted into a historical status when any of the
    following conditions are met:

    - The task is marked as completed.
    - There is a change in the task's phase or description.
    - A specified time interval has elapsed.
    """

    task_id: str
    """
    A unique identifier for the training task.
    """

    phase: str
    """
    The current phase of the task (e.g., 'initializing', 'training', 'completed').
    """

    progress: float
    """
    The task's progress as a percentage (0.0 to 100.0).
    """

    description: str
    """
    Additional details about the task's current status.
    """

    is_complete: bool
    """
    Indicates whether the task has been completed.
    """

    updated_at: datetime
    """
    The timestamp of the last status update.
    """


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


@dataclass
class TrainingTask[IdType: (str, None) = str]:
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
            │   ├── base
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
