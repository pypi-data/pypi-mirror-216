import dataclasses
from enum import Enum
from typing import Optional

from dt_duckiematrix_messages import CBorMessage


class NetworkEndpointType(Enum):
    DATA_IN = "data_in"
    DATA_OUT = "data_out"
    CONTROL_IN = "control_in"
    CONTROL_OUT = "control_out"


class NetworkEndpointProtocol(Enum):
    TCP = "tcp"
    UDP = "udp"


@dataclasses.dataclass
class NetworkEndpoint(CBorMessage):
    protocol: str
    hostname: Optional[str]
    port: int

    def to_uri(self, hostname: Optional[str]) -> str:
        hostname = self.hostname if self.hostname else hostname
        if self.protocol == "icp":
            return f"{self.protocol}://{hostname}"
        else:
            return f"{self.protocol}://{hostname}:{self.port}"
