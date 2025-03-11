from mlops.protos import worker_pb2, worker_pb2_grpc, messages_pb2
from mlops.worker.interfaces import WorkerBase


class WorkerServicer(worker_pb2_grpc.WorkerServicer):
    def __init__(self, worker: WorkerBase):
        self.worker = worker

    def GetStatus(self, request: None, context) -> messages_pb2.WorkerStatus:  # noqa: N802
        return super().GetStatus(request, context)

    def StartWorker(self, request: worker_pb2.StartWorkerRequest, context) -> None:  # noqa: N802
        return super().StartWorker(request, context)

    def StopWorker(self, request: None, context) -> None:  # noqa: N802
        return super().StopWorker(request, context)
