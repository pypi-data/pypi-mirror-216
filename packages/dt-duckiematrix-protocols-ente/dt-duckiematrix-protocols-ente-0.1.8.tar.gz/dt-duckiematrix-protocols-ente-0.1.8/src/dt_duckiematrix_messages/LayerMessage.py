import dataclasses
from typing import Dict, Any

from dt_duckiematrix_messages import CBorMessage


@dataclasses.dataclass
class LayerMessage(CBorMessage):
    content: Dict[str, Any]
