from concurrent import futures
import grpc
from protos import test_pb2, test_pb2_grpc
from google.protobuf import empty_pb2


def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    test_pb2_grpc.add_TestServicer_to_server(TestServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


class TestServicer(test_pb2_grpc.TestServicer):
    def Echo(
        self, request: test_pb2.TestData, context: grpc.ServicerContext
    ) -> test_pb2.TestData:
        return request

    def RequestEmpty(
        self, request: empty_pb2.Empty, context: grpc.ServicerContext
    ) -> empty_pb2.Empty:
        return request

    def Repeated(
        self, request: test_pb2.RepeatedData, context: grpc.ServicerContext
    ) -> test_pb2.RepeatedData:
        return request


if __name__ == "__main__":
    main()
