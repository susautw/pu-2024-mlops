from dataclasses import dataclass
from typing import NamedTuple

from mlops.common.model import WorkerStatus


class WorkerConnectionInfo(NamedTuple):
    host: str
    port: int


@dataclass
class WorkerRecord:
    status: WorkerStatus

    connection: WorkerConnectionInfo

    current_task_id: str | None
    """
    The current task id assigned to the worker.

    Worker storage SHOULD NOT use this worker id to assign new tasks
    if this field is not None.

    This field should be set when assigning a task to the worker
    and cleared when the worker is done with the task. 
    """
