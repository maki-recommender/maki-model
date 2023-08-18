from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Item(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class RecommendedItem(_message.Message):
    __slots__ = ["id", "score"]
    ID_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    id: int
    score: float
    def __init__(self, id: _Optional[int] = ..., score: _Optional[float] = ...) -> None: ...

class WatchedAnime(_message.Message):
    __slots__ = ["items", "k"]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    K_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[Item]
    k: int
    def __init__(self, items: _Optional[_Iterable[_Union[Item, _Mapping]]] = ..., k: _Optional[int] = ...) -> None: ...

class RecommendedAnime(_message.Message):
    __slots__ = ["items"]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[RecommendedItem]
    def __init__(self, items: _Optional[_Iterable[_Union[RecommendedItem, _Mapping]]] = ...) -> None: ...
