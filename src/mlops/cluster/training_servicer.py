from mlops.protos import worker_cluster_pb2_grpc, worker_cluster_pb2, messages_pb2


class WorkerClusterTrainingServicer(
    worker_cluster_pb2_grpc.WorkerClusterTrainingServicer
):
    def GetWorkersStatus(  # noqa: N802
        self, request, context
    ) -> worker_cluster_pb2.GetWorkersStatusResponse:
        return super().GetWorkersStatus(request, context)

    def GetWorkerStatus(  # noqa: N802
        self, request: worker_cluster_pb2.GetWorkerStatusRequest, context
    ) -> messages_pb2.WorkerStatus:
        return super().GetWorkerStatus(request, context)

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
