from abc import ABC, abstractmethod
from dataclasses import dataclass

from mlops.common.model import WorkerStatus


@dataclass
class WorkerStartOptions:
    task_path: str


class WorkerBase(ABC):
    """
    Base class for all workers

    The worker is responsible for executing a task without communication with DB or other services.
    Its can only communicate with File System or other local resources.
    """

    @abstractmethod
    def get_status(self) -> WorkerStatus:
        """
        Get the current status of the worker

        :return: a WorkerStatus object
        """

    @abstractmethod
    def start(self, options: WorkerStartOptions) -> None:
        """
        Start the worker

        :param options: WorkerStartOptions object
        """

    @abstractmethod
    def stop(self) -> None:
        """
        Stop the worker
        """

    @abstractmethod
    def init(self, worker_id: str) -> None:
        """
        Initialize the worker

        :param worker_id: a unique identifier for the worker
        """

    @abstractmethod
    def shutdown(self) -> None:
        """
        Close the worker
        """
