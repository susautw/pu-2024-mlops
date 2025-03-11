from mlops.protos import worker_cluster_pb2_grpc, worker_cluster_pb2, messages_pb2


class WorkerClusterWorkerServicer(worker_cluster_pb2_grpc.WorkerClusterWorkerServicer):
    def CheckIn(  # noqa: N802
        self, request: messages_pb2.WorkerData, context
    ) -> worker_cluster_pb2.CheckInResponse:
        return super().CheckIn(request, context)

    def ReportStatus(  # noqa: N802
        self, request: worker_cluster_pb2.ReportStatusRequest, context
    ) -> None:
        return super().ReportStatus(request, context)

    def ReportTrainingStatus(  # noqa: N802
        self, request: worker_cluster_pb2.ReportTrainingStatusRequest, context
    ) -> None:
        return super().ReportTrainingStatus(request, context)
