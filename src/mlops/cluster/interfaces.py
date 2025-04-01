from abc import ABC, abstractmethod

from mlops.common.model import WorkerStatus, TrainingStatus, WorkerData


class WorkerClusterTrainingControllerBase(ABC):
    """
    Worker cluster interface for managing training tasks
    """

    @abstractmethod
    def get_workers_status(self) -> list[WorkerStatus]:
        """
        Get the status of all workers in the cluster

        :return: list of WorkerStatus objects
        """

    @abstractmethod
    def get_worker_status(self, worker_id: str) -> WorkerStatus | None:
        """
        Get the status of a specific worker

        If the worker has no updates for a while, the cluster should consider to force
        update the worker status

        :param worker_id: the worker id
        :return: WorkerStatus object or None if worker not found
        :raises TimeoutError: if the operation times out
        """

    @abstractmethod
    def assign_training_task(self, task_id: str) -> WorkerStatus | None:
        """
        Assign a training task to a worker

        :param task_id: the training task id
        :return: WorkerStatus object or None if no worker available
        :raises TimeoutError: if the operation times out
        """

    @abstractmethod
    def get_training_status(self, task_id: str) -> TrainingStatus | None:
        """
        Get the status of a training task

        :param task_id: id of the training task
        :return: TrainingStatus object or None if task not found
        """

    @abstractmethod
    def pause_training_task(self, task_id: str) -> None:
        """
        Pause a training task

        No operation if the task is already paused or completed or not found

        :param task_id: id of the training task
        :raises TimeoutError: if the operation times out
        """


class WorkerClusterWorkerControllerBase(ABC):
    """
    Worker cluster interface for managing workers
    """

    @abstractmethod
    def check_in(self, worker_data: WorkerData) -> str:
        """
        Check in a worker

        :param worker_data: WorkerData object
        :return: worker id assigned to the worker (a UUID)
        """

    @abstractmethod
    def report_status(self, worker_status: WorkerStatus) -> None:
        """
        Report worker status

        :param worker_status: WorkerStatus object
        """

    @abstractmethod
    def report_training_status(
        self, worker_id: str, training_status: TrainingStatus | None
    ) -> None:
        """
        Report training status

        :param worker_id: the worker id
        :param training_status: TrainingStatus object or None if no training task assigned
        """


class WorkerClusterBase(
    WorkerClusterTrainingControllerBase, WorkerClusterWorkerControllerBase, ABC
):
    """
    Worker cluster interface for managing workers and training tasks
    """
