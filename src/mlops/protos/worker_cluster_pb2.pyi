import messages_pb2 as _messages_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetWorkersStatusResponse(_message.Message):
    __slots__ = ("statuses",)
    STATUSES_FIELD_NUMBER: _ClassVar[int]
    statuses: _containers.RepeatedCompositeFieldContainer[_messages_pb2.WorkerStatus]
    def __init__(self, statuses: _Optional[_Iterable[_Union[_messages_pb2.WorkerStatus, _Mapping]]] = ...) -> None: ...

class GetWorkerStatusRequest(_message.Message):
    __slots__ = ("worker_id",)
    WORKER_ID_FIELD_NUMBER: _ClassVar[int]
    worker_id: str
    def __init__(self, worker_id: _Optional[str] = ...) -> None: ...

class TaskRequest(_message.Message):
    __slots__ = ("task_id",)
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    task_id: str
    def __init__(self, task_id: _Optional[str] = ...) -> None: ...

class CheckInResponse(_message.Message):
    __slots__ = ("uuid",)
    UUID_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    def __init__(self, uuid: _Optional[str] = ...) -> None: ...

class ReportStatusRequest(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: _messages_pb2.WorkerStatus
    def __init__(self, status: _Optional[_Union[_messages_pb2.WorkerStatus, _Mapping]] = ...) -> None: ...

class ReportTrainingStatusRequest(_message.Message):
    __slots__ = ("worker_id", "status")
    WORKER_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    worker_id: str
    status: _messages_pb2.TrainingStatus
    def __init__(self, worker_id: _Optional[str] = ..., status: _Optional[_Union[_messages_pb2.TrainingStatus, _Mapping]] = ...) -> None: ...
