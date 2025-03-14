from abc import ABC, abstractmethod
from contextlib import AbstractContextManager


class TransactionBase[S](AbstractContextManager[S], ABC):
    """
    Interface for transaction classes

    Transaction classes are used to perform atomic operations on a storage.
    """

    @abstractmethod
    def __enter__(self) -> S:
        """
        Enter the transaction context.

        :return: The storage object that is being used in the transaction.
        """
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Exit the transaction context.

        commits the transaction if no exception is raised,
        otherwise rolls back the transaction.

        :param exc_type: The type of the exception raised, if any.
        :param exc_val: The value of the exception raised, if any.
        :param exc_tb: The traceback of the exception raised, if any.
        :return: None
        """
        pass
