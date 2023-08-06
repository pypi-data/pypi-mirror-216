from typing import Dict

import dataclasses

from dt_duckiematrix_messages import CBorMessage


@dataclasses.dataclass
class WheelsCommand(CBorMessage):
    wheels: Dict[str, float]

@dataclasses.dataclass
class PWMWheelsCommand(CBorMessage):
    wheels: Dict[str, float]
