from abc import ABC, abstractmethod

from mlops.common.model import TrainingStatus


class TrainingStatusStorageBase(ABC):
    """
    Interface for training status storage classes

    Training status storage classes are used to store, cache and manage training status
    information in a cluster.
    """

    @abstractmethod
    def get(self, task_id: str) -> TrainingStatus | None:
        """
        Get training status by task id

        :param task_id: id of the training task
        :return: TrainingStatus object if exists, None otherwise
        """

    @abstractmethod
    def save(self, training_status: TrainingStatus) -> None:
        """
        Save training status

        :param training_status: TrainingStatus object
        """

    @abstractmethod
    def delete(self, task_id: str) -> bool:
        """
        Delete training status by task id

        :param task_id: id of the training task
        :return: True if training status was deleted, False otherwise
        """
