from abc import ABC, abstractmethod

from mlops.cluster.model import WorkerRecord
from mlops.cluster.storages import CommonStorageBase


class WorkerStorageBase(CommonStorageBase[str, WorkerRecord], ABC):
    """
    Interface for worker storage classes

    Worker storage classes are used to store, cache and manage worker information in a cluster
    """

    @abstractmethod
    def save(self, worker_record: WorkerRecord) -> None:
        """
        save worker status

        :param worker_record: WorkerRecord object
        """

    @abstractmethod
    def delete(self, worker_id: str) -> bool:
        """
        Delete worker record by worker id

        :param worker_id: id of worker
        :return: True if worker was deleted, False otherwise
        """

    @abstractmethod
    def get_first_idle_by_type(self, task_type: str) -> WorkerRecord | None:
        """
        Get first idle worker by worker type

        :param worker_type: type of worker
        :return: WorkerStatus object if idle worker exists, None otherwise
        """

    @abstractmethod
    def cleanup(self) -> None:
        """
        Cleanup worker storage. Remove all workers that are not alive (unhealthy)
        """
