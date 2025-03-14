from abc import ABC, abstractmethod
from collections.abc import Callable, Iterable, MutableMapping
from typing import Self

from mlops.cluster.storages import TransactionBase


class CommonStorageBase[K, V](MutableMapping[K, V], ABC):
    """
    Interface for common storage classes

    Common storage classes are used to store, cache and manage common information in a cluster
    """

    @abstractmethod
    def transaction(self) -> TransactionBase[Self]:
        """
        Create a transaction context manager for the storage.
        This method should be implemented to provide a context manager that can be used to
        perform atomic operations on the storage.

        :return: A context manager for the transaction.
        """

    def get_for_update(self, key: K) -> V:
        """
        Get an item from the storage for update.

        .. note::
            This method should be used within a transaction context.

            The item will be locked for update until the transaction is exited.

            If the transaction is committed, the changes will be saved.

            If the transaction is rolled back, the changes will be discarded.

        :param key: The key of the item to get.
        :param predicate: A predicate function to filter the item.
        :return: The item associated with the key.
        :raises KeyError: If the key does not exist in the storage.
        """
        return self[key]

    @abstractmethod
    def search_for_update(self, predicate: Callable[[K, V], bool], *, limit: int | None) -> Iterable[tuple[K, V]]:
        """
        Search for an item in the storage for update.

        .. note::
            This method should be used within a transaction context.

            Returned items will be locked for update until the transaction is exited.

            If the transaction is committed, the changes will be saved.

            If the transaction is rolled back, the changes will be discarded.

        :param predicate: A predicate function to filter the item.
        :return: The item associated with the key.
        """

    @abstractmethod
    def __setitem__(self, key: K, value: V) -> None:
        """
        Set the value for the given key in the storage.

        .. note::
            This method should be used within a transaction context.

            The changes will be saved or discarded based on the transaction outcome.

            The item will be locked for update until the transaction is exited.

        :param key: The key to set.
        :param value: The value to set for the key.
        """

    @abstractmethod
    def __delitem__(self, key: K) -> None:
        """
        Delete the item associated with the given key from the storage.

        .. note::
            This method should be used within a transaction context.

            The changes will be saved or discarded based on the transaction outcome.

            The item will be locked for update until the transaction is exited.

        :param key: The key of the item to delete.
        :raises KeyError: If the key does not exist in the storage.
        """
