import grpc
from mlops.cluster.interfaces import WorkerClusterBase
from mlops.common.model import WorkerStatus
from mlops.common.utils import to_timestamp
from protos import worker_cluster_pb2_grpc, worker_cluster_pb2, messages_pb2
from google.protobuf import empty_pb2


class WorkerClusterTrainingServicer(
    worker_cluster_pb2_grpc.WorkerClusterTrainingServicer
):
    def __init__(self, worker_cluster: WorkerClusterBase) -> None:
        self._worker_cluster = worker_cluster

    def GetWorkersStatus(  # noqa: N802
        self, request: empty_pb2.Empty, context
    ) -> worker_cluster_pb2.GetWorkersStatusResponse:
        statuses = self._worker_cluster.get_workers_status()
        return worker_cluster_pb2.GetWorkersStatusResponse(
            [self._to_proto_status(status) for status in statuses]
        )

    def _to_proto_status(self, domain_status: WorkerStatus) -> messages_pb2.WorkerStatus:
        return messages_pb2.WorkerStatus(
            id=domain_status.id,
            task_type=domain_status.task_type,
            version=domain_status.version,
            healthy=domain_status.healthy,
            has_task=domain_status.has_task,
            joined_at=to_timestamp(domain_status.joined_at),
            created_at=to_timestamp(domain_status.created_at),
            reported_at=to_timestamp(domain_status.reported_at),
        )

    def GetWorkerStatus(  # noqa: N802
        self, request: worker_cluster_pb2.GetWorkerStatusRequest, context
    ) -> messages_pb2.WorkerStatus:
        status = self._worker_cluster.get_worker_status(worker_id=request.worker_id)
        if status is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Worker {request.worker_id} not found")
            return messages_pb2.WorkerStatus()
        return self._to_proto_status(status)

    def AssignTrainingTask(  # noqa: N802
        self, request: worker_cluster_pb2.TaskRequest, context
    ) -> messages_pb2.WorkerStatus:
        return super().AssignTrainingTask(request, context)

    def GetTrainingStatus(  # noqa: N802
        self, request: worker_cluster_pb2.TaskRequest, context
    ) -> messages_pb2.TrainingStatus:
        return super().GetTrainingStatus(request, context)

    def PauseTrainingTask(  # noqa: N802
        self, request: worker_cluster_pb2.TaskRequest, context
    ) -> None:
        return super().PauseTrainingTask(request, context)
