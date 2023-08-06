import dataclasses
from typing import Dict

from dt_duckiematrix_messages import CBorMessage
from dt_duckiematrix_messages.NetworkEndpoint import NetworkEndpoint
from dt_duckiematrix_types import EngineMode


@dataclasses.dataclass
class NetworkJoined(CBorMessage):
    id: str
    mode: EngineMode
    endpoints: Dict[str, NetworkEndpoint]

    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "mode": self.mode.value,
            "endpoints": {
                k: ep.as_dict() for k, ep in self.endpoints.items()
            }
        }

    @classmethod
    def from_bytes(cls, data: bytes) -> 'NetworkJoined':
        msg = super(NetworkJoined, cls).from_bytes(data)
        msg.mode = EngineMode(msg.mode)
        msg.endpoints = {
            k: NetworkEndpoint(**ep) for k, ep in msg.endpoints.items()
        }
        return msg
