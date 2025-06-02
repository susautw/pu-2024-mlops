from mlops.cluster.interfaces import WorkerClusterBase
from mlops.common.model import TrainingStatus, WorkerData, WorkerStatus
from protos import worker_cluster_pb2_grpc, worker_cluster_pb2, messages_pb2


class WorkerClusterWorkerServicer(worker_cluster_pb2_grpc.WorkerClusterWorkerServicer):
    def __init__(self, worker_cluster: WorkerClusterBase) -> None:
        self._worker_cluster = worker_cluster

    def CheckIn(  # noqa: N802
        self, request: messages_pb2.WorkerData, context
    ) -> worker_cluster_pb2.CheckInResponse:
        uuid = self._worker_cluster.check_in(
            WorkerData(
                host=request.host,
                port=request.port,
                task_type=request.task_type,
                version=request.version,
                options=dict(request.options),
            )
        )
        return worker_cluster_pb2.CheckInResponse(uuid=uuid)

    def ReportStatus(  # noqa: N802
        self, request: worker_cluster_pb2.ReportStatusRequest, context
    ) -> None:
        self._worker_cluster.report_status(
            WorkerStatus(
                id=request.status.id,
                task_type=request.status.task_type,
                healthy=request.status.healthy,
                has_task=request.status.has_task,
                version=request.status.version,
                reported_at=request.status.reported_at.ToDatetime(),
                joined_at=request.status.joined_at.ToDatetime(),
                created_at=request.status.created_at.ToDatetime(),
            )
        )

    def ReportTrainingStatus(  # noqa: N802
        self, request: worker_cluster_pb2.ReportTrainingStatusRequest, context
    ) -> None:
        training_status = request.status
        self._worker_cluster.report_training_status(
            worker_id=request.worker_id,
            training_status=TrainingStatus(
                task_id=training_status.task_id,
                phase=training_status.phase,
                progress=training_status.progress,
                description=training_status.description,
                is_completed=training_status.is_completed,
                updated_at=training_status.updated_at.ToDatetime(),
            )
            if training_status.IsInitialized()
            else None,
        )
