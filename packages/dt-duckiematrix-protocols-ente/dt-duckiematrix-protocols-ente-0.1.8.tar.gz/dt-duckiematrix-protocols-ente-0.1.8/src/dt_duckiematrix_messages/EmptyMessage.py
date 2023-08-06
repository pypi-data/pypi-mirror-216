import dataclasses

from dt_duckiematrix_messages import CBorMessage


@dataclasses.dataclass
class EmptyMessage(CBorMessage):
    __empty__: str = ""
