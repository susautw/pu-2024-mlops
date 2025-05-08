import threading
import time
from mlops.cluster.interfaces import WorkerClusterBase
from mlops.cluster.storages.training_status_storage_base import TrainingStatusStorageBase
from mlops.cluster.storages.worker_storage_base import WorkerStorageBase
from mlops.cluster.worker_bridge import WorkerBridgeFactoryBase
from mlops.common.model import TrainingStatus, WorkerStatus, WorkerData
from mlops.common.repos.interfaces import TrainingTaskRepositoryBase
from mlops.worker.interfaces import WorkerStartOptions


class WorkerCluster(WorkerClusterBase):
    def __init__(  # noqa: PLR0913
        self,
        worker_storage: WorkerStorageBase,
        training_status_storage: TrainingStatusStorageBase,
        worker_bridge_factory: WorkerBridgeFactoryBase,
        task_repo: TrainingTaskRepositoryBase,
        clear_interval: int = 60,
        force_update_threshold: int = 120,
    ):
        self.worker_storage = worker_storage
        self.training_status_storage = training_status_storage
        self.task_repo = task_repo
        self.worker_bridge_factory = worker_bridge_factory
        self.clear_interval = clear_interval
        self.force_update_threshold = force_update_threshold

        self._cleanup_thread = threading.Thread(target=self.__thread_cleanup_workers)
        self._close_event = threading.Event()

    def __thread_cleanup_workers(self):
        """
        A thread ensures that all workers are healthy.

        If a worker is not healthy, remove it from the storage
        """
        while not self._close_event.is_set():
            self.worker_storage.cleanup()

            time.sleep(self.clear_interval)

    def get_workers_status(self) -> list[WorkerStatus]:
        return [w.status for w in self.worker_storage.get_all()]

    def get_worker_status(self, worker_id: str) -> WorkerStatus | None:
        record = self.worker_storage.get(worker_id)
        if record is None:
            return None
        if record.updated_at.timestamp() + self.force_update_threshold < time.time():
            #! force update the worker status
            # TODO research error handling in grpc
            bridge = self.worker_bridge_factory.get_worker_bridge(record.connection)
            status = bridge.get_status()
            record = record.with_status(status)
            self.worker_storage.save(record)
        return record.status

    def assign_training_task(self, task_id: str) -> WorkerStatus | None:
        task = self.task_repo.get_by_id(task_id)
        if task is None:
            return None

        worker = self.worker_storage.get_first_idle_by_type(task.task_type)
        if worker is None:
            return None

        #! assing task id to worker, the assigned task id should be cleared when
        #! the worker is done with the task (reporting status with has_task=False)
        worker = worker.with_task_id(task_id)
        self.worker_storage.save(worker)

        bridge = self.worker_bridge_factory.get_worker_bridge(worker.connection)
        bridge.start(WorkerStartOptions(task_path=str(task.base_dir)))
        # TODO: if error occurs, should clear the task id from the worker record immediately
        # TODO: may also need to mark the worker as unhealthy according to the error

        return worker.status

    def get_training_status(self, task_id: str) -> TrainingStatus | None:
        """
        Get training status by task id

        :param task_id: id of the training task
        :return: TrainingStatus object if exists, None otherwise
        """
        return self.training_status_storage.get(task_id)

    def pause_training_task(self, task_id: str) -> None:
        task = self.task_repo.get_by_id(task_id)
        if task is None:
            return
        # TODO: implement pause training task

    def check_in(self, worker_data: WorkerData) -> str:
        raise NotImplementedError

    def report_status(self, worker_status: WorkerStatus) -> None:
        pass

    def report_training_status(
        self, worker_id: str, training_status: TrainingStatus | None
    ) -> None:
        pass

    def shutdown(self) -> None:
        """
        Shutdown the worker cluster

        This method is idempotent
        """
        self._close_event.set()
        self._cleanup_thread.join()

    def __del__(self):
        """
        Shutdown the worker cluster when the object is deleted
        """
        self.shutdown()
