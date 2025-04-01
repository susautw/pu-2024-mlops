from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from mlops.cluster.interfaces import WorkerClusterWorkerControllerBase
from mlops.common.model import WorkerStatus


@dataclass
class WorkerStartOptions:
    task_path: str  # TODO sep input and output path


@dataclass
class WorkerInitOptions:
    host: str
    port: int
    options: dict[str, Any] = field(default_factory=dict)


class WorkerControllerBase(ABC):
    """
    Base class for all worker controllers
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


class WorkerBase(WorkerControllerBase, ABC):
    """
    Base class for all workers

    The worker is responsible for executing a task without communication with DB or other services.
    Its can only communicate with File System or other local resources.
    """

    @abstractmethod
    def init(
        self, cluster: WorkerClusterWorkerControllerBase, options: WorkerInitOptions
    ) -> None:
        """
        Initialize the worker

        :param cluster: WorkerClusterWorkerControllerBase object
        :param options: WorkerInitOptions object
        """

    @abstractmethod
    def shutdown(self) -> None:
        """
        Close the worker
        """
