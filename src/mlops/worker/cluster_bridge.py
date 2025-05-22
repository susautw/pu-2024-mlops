from google.protobuf import struct_pb2

from mlops.cluster.interfaces import WorkerClusterWorkerControllerBase
from mlops.common.model import TrainingStatus, WorkerStatus, WorkerData
from mlops.common.utils import to_timestamp
from mlops.protos import worker_cluster_pb2_grpc, messages_pb2, worker_cluster_pb2


class ClusterBridge(WorkerClusterWorkerControllerBase):
    def __init__(self, stub: worker_cluster_pb2_grpc.WorkerClusterWorkerStub):
        self.stub = stub

    def check_in(self, worker_data: WorkerData) -> str:
        options = struct_pb2.Struct()
        options.update(worker_data.options)
        return self.stub.CheckIn(
            messages_pb2.WorkerData(
                host=worker_data.host,
                port=worker_data.port,
                task_type=worker_data.task_type,
                options=options,
            )
        ).uuid

    def report_status(self, worker_status: WorkerStatus) -> None:
        self.stub.ReportStatus(
            messages_pb2.WorkerStatus(
                id=worker_status.id,
                task_type=worker_status.task_type,
                healthy=worker_status.healthy,
                has_task=worker_status.has_task,
                joined_at=to_timestamp(worker_status.joined_at),
                created_at=to_timestamp(worker_status.created_at),
            )
        )

    def report_training_status(
        self, worker_id: str, training_status: TrainingStatus | None
    ) -> None:
        self.stub.ReportTrainingStatus(
            worker_cluster_pb2.ReportTrainingStatusRequest(
                worker_id=worker_id,
                status=messages_pb2.TrainingStatus(
                    task_id=training_status.task_id,
                    phase=training_status.phase,
                    progress=training_status.progress,
                    description=training_status.description,
                    is_completed=training_status.is_complete,
                )
                if training_status is not None
                else None,
            )
        )
