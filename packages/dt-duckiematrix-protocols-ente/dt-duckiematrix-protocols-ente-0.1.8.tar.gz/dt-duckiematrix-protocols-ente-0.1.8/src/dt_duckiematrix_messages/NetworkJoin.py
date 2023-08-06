import dataclasses
from typing import Optional

from dt_duckiematrix_messages import CBorMessage


@dataclasses.dataclass
class NetworkJoin(CBorMessage):
    role: int
    group: str
    key: Optional[str]
    location: str
