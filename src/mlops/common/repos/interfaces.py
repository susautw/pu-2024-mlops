from abc import ABC, abstractmethod

from mlops.common.model import TrainingTask


class TrainingTaskRepositoryBase(ABC):
    @abstractmethod
    def get_by_id(self, task_id: int) -> TrainingTask:
        """
        Get a task by its id

        :param task_id: id of the task
        :return: TrainingTask object
        :raises RepoError: when task retrieval fails
        """

    @abstractmethod
    def create(self, task: TrainingTask[None]) -> TrainingTask:
        """
        Create a task

        :param task: Task to create
        :return: Created task with id assigned or None if failed
        :raises RepoCreateError: when task creation fails
        """

    @abstractmethod
    def update(self, task: TrainingTask) -> TrainingTask:
        """
        Update a task

        :param task: Task to update
        :return: Updated task or None if failed
        :raises RepoUpdateError: when task update fails
        """
