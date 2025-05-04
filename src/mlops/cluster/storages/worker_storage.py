from collections.abc import Iterable, MutableMapping

from mlops.cluster.model import WorkerRecord
from mlops.cluster.storages.worker_storage_base import WorkerStorageBase


# TODO: create a Redis worker storage
class WorkerStorage(WorkerStorageBase):
    """
    A simple in-memory worker storage implementation.

    .. warning:: This storage is not thread-safe.
    """

    def __init__(self, storage: MutableMapping[str, WorkerRecord]) -> None:
        self._workers = storage

    def get(self, worker_id: str) -> WorkerRecord | None:
        """
        Get worker record by worker id

        :param worker_id: id of worker
        :return: WorkerRecord object if exists, None otherwise
        """
        return self._workers.get(worker_id, None)

    def get_all(self) -> Iterable[WorkerRecord]:
        """
        Get all worker records

        :return: list of WorkerRecord objects
        """
        return self._workers.values()

    def save(self, worker_record: WorkerRecord):
        if worker_record.status.id in self._workers:
            data_version = self._workers[worker_record.status.id].data_version
            if worker_record.data_version < data_version:
                return  # ignore old data

        # update the worker record
        self._workers[worker_record.status.id] = worker_record

    def get_first_idle_by_type(self, task_type: str) -> WorkerRecord | None:
        for workers in self._workers.values():
            if (
                workers.status.healthy
                and not workers.status.has_task
                and workers.status.task_type == task_type
            ):
                return workers
        return None

    def cleanup(self):
        """
        Cleanup worker storage. Remove all workers that are not alive (unhealthy)
        """
        for worker_id in list(self._workers.keys()):
            if not self._workers[worker_id].status.healthy:
                del self._workers[worker_id]

    def delete(self, worker_id: str) -> bool:
        return self._workers.pop(worker_id, None) is not None
