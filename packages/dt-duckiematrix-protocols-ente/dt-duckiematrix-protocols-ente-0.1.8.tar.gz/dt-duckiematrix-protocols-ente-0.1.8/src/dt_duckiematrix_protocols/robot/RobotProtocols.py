from abc import ABC

from dt_duckiematrix_types import EngineMode
from dt_duckiematrix_protocols.commons.CBORProtocol import CBORProtocol


class RobotProtocolAbs(CBORProtocol, ABC):

    def __init__(self, engine_hostname: str, auto_commit: bool = False):
        super(RobotProtocolAbs, self).__init__(engine_hostname, "robot", auto_commit)


class GymRobotProtocol(RobotProtocolAbs):

    def __init__(self, engine_hostname: str, auto_commit: bool = False):
        super(GymRobotProtocol, self).__init__(engine_hostname, auto_commit)

    def validate_engine_mode(self, mode: EngineMode) -> bool:
        return mode == EngineMode.GYM


class RealtimeRobotProtocol(RobotProtocolAbs):

    def __init__(self, engine_hostname: str, auto_commit: bool = False):
        super(RealtimeRobotProtocol, self).__init__(engine_hostname, auto_commit)

    def validate_engine_mode(self, mode: EngineMode) -> bool:
        return mode == EngineMode.REALTIME
