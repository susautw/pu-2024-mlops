from abc import ABC


class TrainingStatusStorageBase(ABC):
    """
    Interface for training status storage classes

    Training status storage classes are used to store, cache and manage training status
    information in a cluster.
    """
