from mlops.cluster.model import WorkerRecord
from mlops.cluster.storages.interfaces import WorkerStorageBase


# TODO make it thread-safe
class MemoryWorkerStorage(WorkerStorageBase):
    """
    In-memory storage for worker status.
    It's not thread-safe.
    """

    def __init__(self):
        self.workers: dict[str, WorkerRecord] = {}

    def get(self, worker_id: str) -> WorkerRecord | None:
        return self.workers.get(worker_id)

    def get_all(self) -> list[WorkerRecord]:
        return list(self.workers.values())

    def delete(self, worker_id: str) -> bool:
        return self.workers.pop(worker_id, None) is not None

    def save(self, worker_record: WorkerRecord):
        self.workers[worker_record.status.id] = worker_record

    def clear(self) -> None:
        self.workers.clear()

    def get_first_idle_by_type(self, task_type: str) -> WorkerRecord | None:
        for worker in self.workers.values():
            status = worker.status
            if status.healthy and status.has_task is False and status.task_type == task_type:
                return worker
        return None

    def cleanup(self):
        for worker_id in list(self.workers.keys()):
            if not self.workers[worker_id].status.healthy:
                del self.workers[worker_id]
