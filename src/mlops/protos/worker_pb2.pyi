from google.protobuf import empty_pb2 as _empty_pb2
import messages_pb2 as _messages_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class StartWorkerRequest(_message.Message):
    __slots__ = ("task_path",)
    TASK_PATH_FIELD_NUMBER: _ClassVar[int]
    task_path: str
    def __init__(self, task_path: _Optional[str] = ...) -> None: ...
