import dataclasses

from dt_duckiematrix_messages import CBorMessage


@dataclasses.dataclass
class NetworkReady(CBorMessage):
    id: str
    role: int
    key: str
