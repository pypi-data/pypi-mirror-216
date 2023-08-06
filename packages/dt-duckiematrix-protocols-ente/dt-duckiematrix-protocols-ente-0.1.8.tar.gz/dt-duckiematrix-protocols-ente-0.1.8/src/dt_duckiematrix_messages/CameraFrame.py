import dataclasses
import numpy as np

from dt_duckiematrix_messages import CBorMessage


@dataclasses.dataclass
class CameraFrame(CBorMessage):
    format: str
    width: int
    height: int
    frame: bytes

    @classmethod
    def from_jpeg(cls, jpeg: bytes) -> 'CameraFrame':
        return CameraFrame("jpeg", 0, 0, jpeg)

    def as_uint8(self) -> np.ndarray:
        return np.frombuffer(self.frame, np.uint8)
