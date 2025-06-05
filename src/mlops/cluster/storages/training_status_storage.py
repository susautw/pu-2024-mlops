from mlops.cluster.worker_cluster import TrainingStatusStorageBase
from mlops.common.model import TrainingStatus


class TrainingStatusStorage(TrainingStatusStorageBase):
    _storage: dict[str, TrainingStatus]

    def __init__(self):
        self._storage = {}

    def get(self, task_id: str) -> TrainingStatus | None:
        return self._storage.get(task_id)

    def save(self, training_status: TrainingStatus) -> None:
        # Don't overwrite existing training status if it is newer
        if (
            training_status.task_id in self._storage
            and self._storage[training_status.task_id].updated_at
            >= training_status.updated_at
        ):
            return

        self._storage[training_status.task_id] = training_status

    def delete(self, task_id: str) -> bool:
        if task_id in self._storage:
            del self._storage[task_id]
            return True
        return False
