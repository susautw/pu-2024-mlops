import argparse

import grpc

from mlops.protos import worker_cluster_pb2_grpc
from mlops.worker.cluster_bridge import ClusterBridge
from mlops.worker.interfaces import WorkerInitOptions
from mlops.worker.testing_worker import TestingWorker


def main():
    worker = TestingWorker()

    print(f'Worker started: {worker}')

    with grpc.insecure_channel("localhost:50000") as channel:
        stub = worker_cluster_pb2_grpc.WorkerClusterWorkerStub(channel)
        cluster = ClusterBridge(stub)

        worker.init(cluster, WorkerInitOptions(
            host='0.0.0.0',
            port=50051,
        ))




def get_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Start a worker')
    parser.add_argument('--config', type=str, help='Path to the config file')

    return parser


if __name__ == '__main__':
    main()
