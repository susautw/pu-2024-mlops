from collections.abc import Callable, Iterable, Iterator
from typing import Self, overload
from mlops.cluster.model import WorkerRecord
from mlops.cluster.storages import CommonStorageBase, TransactionBase
from mlops.cluster.storages.worker_storage_base import WorkerStorageBase


class WorkerStorage(WorkerStorageBase):
    """
    Storage for worker status.

    .. warning:: This storage is not thread-safe.
    """

    def __init__(self, storage: CommonStorageBase[str, WorkerRecord]) -> None:
        self._workers = storage

    def save(self, worker_record: WorkerRecord):
        self._workers[worker_record.status.id] = worker_record

    def get_first_idle_by_type(self, task_type: str) -> WorkerRecord | None:
        workers = list(
            self._workers.search_for_update(
                lambda _, v: v.status.healthy
                and v.status.has_task is False
                and v.status.task_type == task_type,
                limit=1,
            )
        )
        worker = workers[0] if len(workers) > 0 else None
        if worker is not None:
            return worker[1]
        return None

    def cleanup(self):
        for worker_id, _ in list(
            self._workers.search_for_update(lambda _, v: not v.status.healthy)
        ):
            self.delete(worker_id)

    def __iter__(self) -> Iterator[str]:
        return iter(self._workers)

    def __len__(self) -> int:
        return len(self._workers)

    def __getitem__(self, key: str) -> WorkerRecord:
        return self._workers[key]

    def __setitem__(self, key: str, value: WorkerRecord) -> None:
        self._workers[key] = value

    def __delitem__(self, key: str) -> None:
        del self._workers[key]

    def transaction(self) -> TransactionBase[Self]:
        return _Transaction(self)

    def delete(self, worker_id: str) -> bool:
        return self._workers.pop(worker_id, None) is not None

    def search_for_update(
        self, predicate: Callable[[str, WorkerRecord], bool], *, limit: int | None = None
    ) -> Iterable[tuple[str, WorkerRecord]]:
        return self._workers.search_for_update(predicate, limit=limit)

    @overload
    def get_for_update(self, key: str) -> WorkerRecord: ...

    @overload
    def get_for_update[D](self, key: str, default: D) -> WorkerRecord | D: ...

    def get_for_update[D](
        self, key: str, default: D = NotImplemented
    ) -> WorkerRecord | D:
        return self._workers.get_for_update(key, default=default)


class _Transaction(TransactionBase):
    def __init__(self, storage: "WorkerStorage") -> None:
        self._underlying_tx = storage.transaction()

    def __enter__(self) -> "WorkerStorage":
        return WorkerStorage(self._underlying_tx.__enter__())

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self._underlying_tx.__exit__(exc_type, exc_val, exc_tb)
