import dataclasses

from dt_duckiematrix_messages import CBorMessage


@dataclasses.dataclass
class NetworkLeave(CBorMessage):
    id: str
