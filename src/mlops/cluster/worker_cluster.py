import threading
import time
from mlops.cluster.interfaces import WorkerClusterBase
from mlops.cluster.storages.worker_storage_base import WorkerStorageBase
from mlops.cluster.worker_bridge import WorkerBridgeFactoryBase
from mlops.common.model import TrainingStatus, WorkerStatus, WorkerData
from mlops.common.repos.interfaces import TrainingTaskRepositoryBase
from mlops.worker.interfaces import WorkerStartOptions


class WorkerCluster(WorkerClusterBase):
    def __init__(
        self,
        storage: WorkerStorageBase,
        worker_bridge_factory: WorkerBridgeFactoryBase,
        task_repo: TrainingTaskRepositoryBase,
        clear_interval: int = 60,
    ):
        self.storage = storage
        self.task_repo = task_repo
        self.worker_bridge_factory = worker_bridge_factory
        self.clear_interval = clear_interval

        self._cleanup_thread = threading.Thread(target=self.__thread_cleanup_workers)
        self._close_event = threading.Event()

    def __thread_cleanup_workers(self):
        """
        A thread ensures that all workers are healthy.

        If a worker is not healthy, remove it from the storage
        """
        while not self._close_event.is_set():
            with self.storage.transaction() as tx:
                tx.cleanup()
            time.sleep(self.clear_interval)

    def get_workers_status(self) -> list[WorkerStatus]:
        return [w.status for w in self.storage.values()]

    def get_worker_status(self, worker_id: str) -> WorkerStatus | None:
        record = self.storage.get(worker_id)
        if record is None:
            return None
        return record.status

    def assign_training_task(self, task_id: str) -> WorkerStatus | None:
        task = self.task_repo.get_by_id(task_id)

        with self.storage.transaction() as tx:
            worker = tx.get_first_idle_by_type(task.task_type)
            if worker is None:
                return None

            bridge = self.worker_bridge_factory.get_worker_bridge(worker.connection)
            bridge.start(WorkerStartOptions(task_path=str(task.base_dir)))

            #! assing task id to worker, the assigned task id should be cleared when
            #! the worker is done with the task (reporting status with has_task=False)
            worker = worker.with_task_id(task_id)
            tx.save(worker)

        return worker.status

    def get_training_status(self, task_id: str) -> TrainingStatus | None:
        pass

    def pause_training_task(self, task_id: str) -> None:
        pass

    def check_in(self, worker_data: WorkerData) -> str:
        raise NotImplementedError

    def report_status(self, worker_status: WorkerStatus) -> None:
        pass

    def report_training_status(self, worker_id: str, training_status: TrainingStatus | None) -> None:
        pass

    def __del__(self):
        """
        End and join the cleanup thread when the object is deleted
        """
        self._close_event.set()
        self._cleanup_thread.join()
