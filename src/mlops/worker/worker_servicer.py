from google.protobuf import empty_pb2
import grpc
from mlops.common.utils import to_timestamp
from mlops.protos import worker_pb2, worker_pb2_grpc, messages_pb2
from mlops.worker.interfaces import WorkerBase, WorkerStartOptions


class WorkerServicer(worker_pb2_grpc.WorkerServicer):
    def __init__(self, worker: WorkerBase):
        self.worker = worker

    def GetStatus(  # noqa: N802
        self, request: empty_pb2.Empty, context: grpc.ServicerContext
    ) -> messages_pb2.WorkerStatus:
        worker_status = self.worker.get_status()
        return messages_pb2.WorkerStatus(
            id=worker_status.id,
            task_type=worker_status.task_type,
            version=worker_status.version,
            healthy=worker_status.healthy,
            has_task=worker_status.has_task,
            joined_at=to_timestamp(worker_status.joined_at),
            created_at=to_timestamp(worker_status.created_at),
            reported_at=to_timestamp(worker_status.reported_at),
        )

    def StartWorker(  # noqa: N802
        self, request: worker_pb2.StartWorkerRequest, context: grpc.ServicerContext
    ) -> empty_pb2.Empty:
        self.worker.start(WorkerStartOptions(request.task_path))
        return empty_pb2.Empty()

    def StopWorker(  # noqa: N802
        self, request: empty_pb2.Empty, context: grpc.ServicerContext
    ) -> empty_pb2.Empty:
        self.worker.stop()
        return empty_pb2.Empty()
