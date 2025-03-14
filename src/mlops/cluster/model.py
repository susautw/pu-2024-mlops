from typing import NamedTuple

from mlops.common.model import WorkerStatus


class WorkerConnectionInfo(NamedTuple):
    host: str
    port: int


class WorkerRecord(NamedTuple):
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

    def with_status(self, status: WorkerStatus) -> "WorkerRecord":
        return WorkerRecord(status, self.connection, self.current_task_id)

    def with_task_id(self, task_id: str | None) -> "WorkerRecord":
        return WorkerRecord(self.status, self.connection, task_id)
