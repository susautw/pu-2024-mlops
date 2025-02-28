from mlops.cluster.interfaces import WorkerClusterBase
from mlops.cluster.storages.interfaces import WorkerStorageBase
from mlops.cluster.worker_bridge import WorkerBridgeFactoryBase
from mlops.common.model import TrainingStatus, WorkerStatus, WorkerData
from mlops.common.repos.interfaces import TrainingTaskRepositoryBase
from mlops.worker.interfaces import WorkerStartOptions


class WorkerCluster(WorkerClusterBase):

    def __init__(
            self,
            storage: WorkerStorageBase,
            worker_bridge_factory: WorkerBridgeFactoryBase,
            task_repo: TrainingTaskRepositoryBase
    ):
        self.storage = storage
        self.task_repo = task_repo
        self.worker_bridge_factory = worker_bridge_factory

    def get_workers_status(self) -> list[WorkerStatus]:
        return [w.status for w in self.storage.get_all()]

    def get_worker_status(self, worker_id: str) -> WorkerStatus | None:
        record = self.storage.get(worker_id)
        if record is None:
            return None
        return record.status

    def assign_training_task(self, task_id: int) -> WorkerStatus | None:
        task = self.task_repo.get_by_id(task_id)
        worker = self.storage.get_first_idle_by_type(task.task_type)
        if worker is None:
            return None

        bridge = self.worker_bridge_factory.get_worker_bridge(worker.connection)
        bridge.start(WorkerStartOptions(
            task_path=str(task.input_dir)  # TODO: add output dir
        ))

        return worker.status

    def get_training_status(self, task_id: int) -> TrainingStatus | None:
        pass

    def pause_training_task(self, task_id: int) -> None:
        pass

    def check_in(self, worker_data: WorkerData) -> str:
        pass

    def report_status(self, worker_status: WorkerStatus) -> None:
        pass

    def report_training_status(self, worker_id: str, training_status: TrainingStatus | None) -> None:
        pass
