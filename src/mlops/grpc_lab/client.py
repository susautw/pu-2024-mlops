import datetime
import grpc

from mlops.common.utils import to_timestamp
from protos import test_pb2, test_pb2_grpc
from google.protobuf import empty_pb2


def main():
    with grpc.insecure_channel("127.0.0.1:50051") as channel:
        stub = test_pb2_grpc.TestStub(channel)
        try:
            print(
                # stub.Echo(
                #     test_pb2.TestData(
                #         id="abc",
                #         name="",
                #         created_at=to_timestamp(datetime.datetime.now()),
                #         tags=["tag1", "tag2"],
                #         message=None,
                #     )
                # )
                stub.Repeated(
                    test_pb2.RepeatedData(
                        data=[
                            test_pb2.TestData(
                                id="abc",
                                name="a",
                                created_at=to_timestamp(datetime.datetime.now()),
                                tags=None,
                            ),
                            # test_pb2.TestData(
                            #     id="def",
                            #     name="",
                            #     created_at=to_timestamp(datetime.datetime.now()),
                            #     tags=None,
                            #     message=empty_pb2.Empty(),
                            # ),
                        ]
                    )
                ).data
            )
        except grpc.RpcError as e:
            assert isinstance(e, grpc.Call)
            print(f"Call error: {e.code()}, details: {e.details()}")


if __name__ == "__main__":
    main()
