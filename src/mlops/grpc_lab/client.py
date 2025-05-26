import datetime
import grpc

from mlops.common.utils import to_timestamp
from protos import test_pb2, test_pb2_grpc
from google.protobuf import empty_pb2


def main():
    with grpc.insecure_channel("127.0.0.1:50051") as channel:
        stub = test_pb2_grpc.TestStub(channel)

        print(
            stub.Echo(
                test_pb2.TestData(
                    id="abc",
                    name="",
                    created_at=datetime.datetime.now(),
                    tags=["tag1", "tag2"],
                    message=None,
                )
            )
        )


if __name__ == "__main__":
    main()
