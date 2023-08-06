import dataclasses

from dt_duckiematrix_messages import CBorMessage


@dataclasses.dataclass
class WheelEncoderTicks(CBorMessage):
    ticks: int
