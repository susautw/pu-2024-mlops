from typing import NamedTuple

from mlops.common.model import WorkerStatus


class WorkerConnectionInfo(NamedTuple):
    host: str
    port: int


class WorkerRecord(NamedTuple):
    status: WorkerStatus
    connection: WorkerConnectionInfo
