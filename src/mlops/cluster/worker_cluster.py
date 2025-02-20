from mlops.cluster.interfaces import WorkerClusterBase
from mlops.common.model import TrainingStatus, WorkerStatus, WorkerData


class WorkerCluster(WorkerClusterBase):
    def get_workers_status(self) -> list[WorkerStatus]:
        pass

    def get_worker_status(self, worker_id: str) -> WorkerStatus | None:
        pass

    def assign_training_task(self, task_id: int) -> WorkerStatus | None:
        pass

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