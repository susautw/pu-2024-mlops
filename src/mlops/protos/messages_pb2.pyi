from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TrainingStatus(_message.Message):
    __slots__ = ("name", "phase", "progress", "description", "is_completed")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PHASE_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    IS_COMPLETED_FIELD_NUMBER: _ClassVar[int]
    name: str
    phase: str
    progress: float
    description: str
    is_completed: bool
    def __init__(self, name: _Optional[str] = ..., phase: _Optional[str] = ..., progress: _Optional[float] = ..., description: _Optional[str] = ..., is_completed: bool = ...) -> None: ...

class WorkerStatus(_message.Message):
    __slots__ = ("id", "task_type", "healthy", "has_task", "joined_at", "created_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    TASK_TYPE_FIELD_NUMBER: _ClassVar[int]
    HEALTHY_FIELD_NUMBER: _ClassVar[int]
    HAS_TASK_FIELD_NUMBER: _ClassVar[int]
    JOINED_AT_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    task_type: str
    healthy: bool
    has_task: bool
    joined_at: _timestamp_pb2.Timestamp
    created_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., task_type: _Optional[str] = ..., healthy: bool = ..., has_task: bool = ..., joined_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class WorkerData(_message.Message):
    __slots__ = ("host", "port", "task_type", "options")
    HOST_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    TASK_TYPE_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    host: str
    port: int
    task_type: str
    options: _struct_pb2.Struct
    def __init__(self, host: _Optional[str] = ..., port: _Optional[int] = ..., task_type: _Optional[str] = ..., options: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...
