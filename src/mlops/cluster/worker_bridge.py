import threading
import time
import weakref
from abc import ABC, abstractmethod
from datetime import datetime
from typing import NamedTuple

import grpc
from google.protobuf import empty_pb2, timestamp_pb2
from readerwriterlock import rwlock

from mlops.cluster.model import WorkerConnectionInfo
from mlops.common.model import WorkerStatus
from mlops.protos import worker_pb2_grpc, messages_pb2, worker_pb2
from mlops.worker.interfaces import WorkerControllerBase, WorkerStartOptions

__ALL__ = ['WorkerBridgeBase', 'WorkerBridgeFactoryBase', 'WorkerBridge', 'WorkerBridgeFactory']


class WorkerBridgeBase(WorkerControllerBase, ABC):
    @abstractmethod
    def close(self) -> None:
        """
        Close the bridge
        :return:
        """


class WorkerBridgeFactoryBase(ABC):
    """
    Factory for creating or getting worker bridges
    """

    @abstractmethod
    def get_worker_bridge(self, worker_connection_info: WorkerConnectionInfo) -> WorkerBridgeBase:
        """
        Get a worker bridge via the connection info

        :param worker_connection_info:
        :return:
        """


class WorkerBridge(WorkerControllerBase):
    def __init__(self, channel: grpc.Channel):
        self.channel = channel
        self.worker_stub = worker_pb2_grpc.WorkerStub(channel)
        self._finalizer = weakref.finalize(self, self.__finalize)  # Destructor

    def get_status(self) -> WorkerStatus:
        raw_status: messages_pb2.WorkerStatus = self.worker_stub.GetStatus(empty_pb2.Empty())
        return WorkerStatus(
            id=raw_status.id,
            task_type=raw_status.task_type,
            version=raw_status.version,
            healthy=raw_status.healthy,
            has_task=raw_status.has_task,
            joined_at=self._to_datetime(raw_status.joined_at),
            created_at=self._to_datetime(raw_status.created_at),
        )

    def _to_datetime(self, timestamp: timestamp_pb2.Timestamp) -> datetime:
        return timestamp.ToDatetime()

    def start(self, options: WorkerStartOptions) -> None:
        self.worker_stub.StartWorker(
            worker_pb2.StartWorkerRequest(
                task_path=options.task_path
            )
        )

    def stop(self) -> None:
        self.worker_stub.StopWorker(empty_pb2.Empty())

    def __finalize(self) -> None:
        self.channel.close()

    def close(self) -> None:
        self._finalizer()


class CachedWorkerBridgeRecord(NamedTuple):
    bridge: WorkerBridge
    breath: int


class WorkerBridgeFactory(WorkerBridgeFactoryBase):
    _cached_bridges: dict[WorkerConnectionInfo, CachedWorkerBridgeRecord]
    _clean_thread: threading.Thread
    _close_event: threading.Event
    _cache_lock: rwlock.RWLockFair

    INITIAL_BREATH_SEC = 120

    def __init__(self):
        self._cached_bridges = {}
        self._clean_thread = threading.Thread(target=self._clean)
        self._close_event = threading.Event()
        self._cache_lock = rwlock.RWLockFair()

    def _clean(self):
        while not self._close_event.wait(0):
            with self._cache_lock.gen_wlock():
                for key, record in self._cached_bridges.items():
                    record.breath -= 1
                    if record.breath <= 0:
                        record.bridge.close()
                        self._cached_bridges.pop(key, None)
            time.sleep(1)

    def get_worker_bridge(self, worker_connection_info: WorkerConnectionInfo) -> WorkerBridge:
        with self._cache_lock.gen_rlock():
            record = self._cached_bridges.get(worker_connection_info)

        cache_hit = record is not None
        if not cache_hit:
            # Try to create a new bridge
            record = self._create_bridge(worker_connection_info)

        with self._cache_lock.gen_wlock():
            if cache_hit:
                record.breath = self.INITIAL_BREATH_SEC  # Reset the breath
            else:
                # Cache the new bridge or get the bridge from another thread
                record = self._cached_bridges.setdefault(worker_connection_info, record)
        return record.bridge

    def _create_bridge(self, worker_connection_info: WorkerConnectionInfo) -> CachedWorkerBridgeRecord:
        channel = grpc.insecure_channel(f'{worker_connection_info.host}:{worker_connection_info.port}')
        bridge = WorkerBridge(channel)  # channel will be closed by the bridge automatically when it is destructed
        return CachedWorkerBridgeRecord(bridge=bridge, breath=self.INITIAL_BREATH_SEC)
