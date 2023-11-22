from typing import Literal
from typing_extensions import TypedDict, NotRequired

from ...languages import Language


Stage = Literal["triples", "base", "clean", "bridges"]
BatchStatus = Literal["done", "started", "pending", "paused", "failed"]


class Batch(TypedDict):
    triples: BatchStatus
    base: BatchStatus
    clean: BatchStatus
    bridges: BatchStatus


BatchDataMap = dict[str, Batch]
BatchMetadata = dict[Language, BatchDataMap]


class BatchListItem(TypedDict):
    name: str
    triples: BatchStatus
    base: BatchStatus
    clean: BatchStatus
    bridges: BatchStatus
    can_be_paused: bool
    can_be_resumed: bool


class StageParams(TypedDict):
    threshold: NotRequired[float]
    ratio: NotRequired[float]
    batch_size: NotRequired[int]
    size: NotRequired[str]


class BatchParams(TypedDict):
    triples: NotRequired[StageParams]
    base: NotRequired[StageParams]
    clean: NotRequired[StageParams]
    bridges: NotRequired[StageParams]


class BlabKGException(Exception):
    pass
