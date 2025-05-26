import argparse

import grpc
from typing import NamedTuple

from protos import worker_cluster_pb2_grpc
from mlops.worker.cluster_bridge import ClusterBridge
from mlops.worker.interfaces import WorkerInitOptions
from mlops.worker.testing_worker import TestingWorker


def main(argv: list[str] | None = None):
    args = Args(**vars(get_arg_parser().parse_args(argv)))

    # TODO: use a worker factory to create the worker
    worker = TestingWorker()

    print(f"Worker started: {worker}")

    with grpc.insecure_channel(args.cluster_bind) as channel:
        stub = worker_cluster_pb2_grpc.WorkerClusterWorkerStub(channel)
        cluster = ClusterBridge(stub)

        worker.init(
            cluster,
            WorkerInitOptions(
                host=args.host,
                port=args.port,
            ),
        )


class Args(NamedTuple):
    cluster_bind: str
    host: str
    port: int


def get_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Start a worker")
    parser.add_argument(
        "--cluster-bind",
        type=str,
        default="cluster:50000",
        help="The address of the cluster to connect to",
    )
    parser.add_argument("--host", type=str, default="0.0.0.0", help="The host to bind to")
    parser.add_argument("--port", type=int, required=True, help="The port to bind to")

    return parser


if __name__ == "__main__":
    main()
