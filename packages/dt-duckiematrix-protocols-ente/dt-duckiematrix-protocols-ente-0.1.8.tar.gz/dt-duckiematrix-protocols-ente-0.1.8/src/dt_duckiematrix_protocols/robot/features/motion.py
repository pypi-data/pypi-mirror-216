import os
from typing import Optional

from dt_duckiematrix_messages.WheelsCommand import WheelsCommand, PWMWheelsCommand
from dt_duckiematrix_protocols.robot.RobotProtocols import RobotProtocolAbs
from dt_duckiematrix_protocols.robot.features.sensors import WheelEncoder


class DifferentialDrive:

    def __init__(self, protocol: RobotProtocolAbs, key: str):
        self._protocol = protocol
        self._key = key

    def __call__(self, left: float, right: float):
        message = WheelsCommand({
            "left": left,
            "right": right,
        })
        self._protocol.publish(self._key, message)

class PWMDifferentialDrive:

    def __init__(self, protocol: RobotProtocolAbs, key: str):
        self._protocol = protocol
        self._key = key

    def __call__(self, left: float, right: float):
        # TODO: assert that left, right belong to [-1,+1]
        message = PWMWheelsCommand({
            "left": left,
            "right": right,
        })
        self._protocol.publish(self._key, message)


class Wheel:

    def __init__(self, protocol: RobotProtocolAbs, key: str, name: str, encoder: bool = False):
        self._key = key
        self._name = name
        self._protocol = protocol
        self._encoder_key = os.path.join(self._key, f"wheel_encoder_{name}")
        self._encoder = WheelEncoder(protocol, self._encoder_key) if encoder else None

    @property
    def encoder(self) -> Optional[WheelEncoder]:
        return self._encoder


class DifferentialDriveWheels:
    
    def __init__(self, protocol: RobotProtocolAbs, key: str,
                 encoder_left: bool = False, encoder_right: bool = False):
        self._key = key
        self._left_wheel = Wheel(protocol, self._key, "left", encoder_left)
        self._right_wheel = Wheel(protocol, self._key, "right", encoder_right)

    @property
    def left(self) -> Wheel:
        return self._left_wheel

    @property
    def right(self) -> Wheel:
        return self._right_wheel

    def get(self, wheel_name: str) -> Wheel:
        return {
            "left": self._left_wheel,
            "right": self._right_wheel,
        }[wheel_name]
