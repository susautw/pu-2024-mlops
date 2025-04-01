from collections.abc import Callable, Iterable, Iterator
import copy
from dataclasses import dataclass
import threading
from typing import Literal, Self, final, overload
from .. import CommonStorageBase, TransactionBase


class _Marker:
    pass


NO_VALUE = _Marker()
DELETED = _Marker()


@dataclass
class _Entry[V]:
    value: V | _Marker = NO_VALUE
    tx: TransactionBase | None = None
    new_value: V | _Marker = NO_VALUE

    @property
    def dirty_value(self) -> V | _Marker:
        return self.new_value if self.new_value is not NO_VALUE else self.value


@final
class TransactionalDict[K, V](CommonStorageBase[K, V]):
    _data: dict[K, _Entry[V]]
    _cond: threading.Condition
    _tx: TransactionBase[Self] | None
    _timeout: float

    def __init__(self, timeout: float) -> None:
        self._data = {}
        self._cond = threading.Condition()
        self._tx = None
        self._timeout = timeout

    def __iter__(self) -> Iterator[K]:
        with self._cond:
            return iter(self._data)

    def __len__(self) -> int:
        with self._cond:
            return len(self._data)

    def __getitem__(self, key: K) -> V:
        with self._cond:
            v = self._data[key].value

        if isinstance(v, _Marker):
            raise KeyError(key)
        return v

    @overload
    def __get_entry(self, key: K, tx: TransactionBase[Self]) -> _Entry[V] | None: ...
    @overload
    def __get_entry(
        self, key: K, tx: TransactionBase[Self], create: Literal[True]
    ) -> _Entry[V]: ...
    def __get_entry(
        self, key: K, tx: TransactionBase[Self], create: bool = False
    ) -> _Entry[V] | None:
        """
        Get the entry for the key in the transaction context.

        If the entry does not exist, it will be created if `create` is True.

        If the entry is locked by another transaction, the method will wait until the lock is released.

        .. note::
            This method should be called within the self._cond context manager.

        :param key: The key of the entry.
        :param tx: The transaction context.
        :param create: If True, the entry will be created if it does not exist.
        :return: The entry for the key.
        :raises TimeoutError: If the lock is not acquired within the timeout.
        """
        while True:
            entry = self._data.get(key, None)
            if entry is None:
                if not create:
                    return None
                entry = _Entry(tx=tx)
                self._data[key] = entry
            if entry.tx is None:
                entry.tx = tx
            if entry.tx is not tx:
                if not self._cond.wait(timeout=self._timeout):
                    raise TimeoutError(f"Timeout waiting for key {key}")
            else:
                return entry

    def __validate_tx(self) -> TransactionBase[Self]:
        if self._tx is None:
            raise RuntimeError("Operation outside of transaction context")
        return self._tx

    def __setitem__(self, key: K, value: V) -> None:
        tx = self.__validate_tx()
        with self._cond:
            entry = self.__get_entry(key, tx, create=True)
            entry.new_value = value

    def __delitem__(self, key: K) -> None:
        tx = self.__validate_tx()
        with self._cond:
            entry = self.__get_entry(key, tx)
            if entry is None or isinstance(entry.value, _Marker):
                raise KeyError(key)
            entry.new_value = DELETED

    @overload
    def get_for_update(self, key: K) -> V: ...
    @overload
    def get_for_update[D](self, key: K, default: D) -> V | D: ...
    def get_for_update[D](self, key: K, default: D = NotImplemented) -> V | D:
        tx = self.__validate_tx()
        with self._cond:
            if key not in self._data:
                raise KeyError(key)
            entry = self.__get_entry(key, tx)
            if entry is None or isinstance(entry.dirty_value, _Marker):
                if default is not NotImplemented:
                    return default
                raise KeyError(key)
            return entry.dirty_value

    def search_for_update(
        self, predicate: Callable[[K, V], bool], *, limit: int | None = None
    ) -> Iterable[tuple[K, V]]:
        tx = self.__validate_tx()
        results = []
        with self._cond:
            for key, entry in self._data.items():
                if isinstance(entry.value, _Marker):
                    continue
                if entry.tx is self._tx:  # Fast path for already locked entries
                    current_value = entry.dirty_value
                    if not isinstance(current_value, _Marker) and predicate(key, current_value):
                        results.append((key, entry.value))
                        if limit is not None and len(results) >= limit:
                            break
                    continue

                # Slow path for entries that need to be locked

                # Predict if the entry should be locked
                if isinstance(entry.value, _Marker) or not predicate(key, entry.value):
                    continue

                # Try to acquire the key lock
                lock_entry = self.__get_entry(key, tx)

                # Check if the entry is still valid after re-acquiring the lock
                if lock_entry is None:
                    continue

                assert lock_entry.new_value is NO_VALUE, (
                    "New value should be NO_VALUE because this case is processed in the fast path"
                )

                # Read the non-dirty current value
                current_value = lock_entry.value
                # Release the key if the value was changed by another transaction
                if isinstance(current_value, _Marker) or not predicate(key, current_value):
                    self._data[key].tx = None
                    self._cond.notify_all()
                    continue

                results.append((key, lock_entry.value))
                if limit is not None and len(results) >= limit:
                    break
        return results[:limit]

    def transaction(self) -> TransactionBase[Self]:
        if self._tx is not None:
            raise RuntimeError("Transaction already in progress")

        storage = copy.copy(self)  # Create a shallow copy of the storage
        storage._tx = _Transaction(storage)
        return storage._tx


class _Transaction[K, V](TransactionBase):
    def __init__(self, storage: TransactionalDict[K, V]) -> None:
        self._storage = storage
        self._level = 0

    def __enter__(self) -> "TransactionalDict[K, V]":
        if self._level > 0:
            raise RuntimeError("Nested transactions are not supported")
        self._level += 1
        return self._storage

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._level -= 1
        with self._storage._cond:
            for key, entry in self._storage._data.items():
                if entry.tx is not self:
                    continue
                if exc_type is None:  # commit
                    if entry.new_value is DELETED:
                        self._storage._data.pop(key, None)
                    elif entry.new_value is not NO_VALUE:
                        entry.value = entry.new_value
                entry.tx = None
                entry.new_value = NO_VALUE
            self._storage._tx = None
            self._storage._cond.notify_all()
