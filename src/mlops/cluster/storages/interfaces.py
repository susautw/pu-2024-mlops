from abc import ABC, abstractmethod


class WorkerStorageBase(ABC):
    """
    Interface for worker storage classes

    Worker storage classes are used to store, cache and manage worker information in a cluster
    """

    @abstractmethod
    def clear(self):
        pass
