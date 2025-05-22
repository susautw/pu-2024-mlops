from datetime import datetime
from google.protobuf import timestamp_pb2


def to_timestamp(dt: datetime | None) -> timestamp_pb2.Timestamp | None:
    if dt is None:
        return None
    ts = timestamp_pb2.Timestamp()
    ts.FromDatetime(dt)
    return ts
