from threading import Semaphore
from typing import Dict, Type, TypeVar, Optional, Set, Callable

from dt_duckiematrix_protocols.commons.LayerProtocol import LayerProtocol
from dt_duckiematrix_protocols.robot.RobotProtocols import RealtimeRobotProtocol
from dt_duckiematrix_protocols.robot.robots import RobotAbs, DB21M, RobotFeature, DBR4, DB21J, \
    WT18, WT19B, WT19A, WT21B, WT21A, DB18, DB19, DC21, CameraEnabledRobot, WheeledRobot, \
    LightsEnabledRobot, RangeEnabledRobot
from dt_duckiematrix_protocols.utils.Pose3D import Pose3D

T = TypeVar("T")


class RobotsManager:

    def __init__(self, engine_hostname: str, auto_commit: bool = False,
                 robot_protocol: Optional[RealtimeRobotProtocol] = None,
                 layer_protocol: Optional[LayerProtocol] = None):
        self._robots: Dict[str, RobotAbs] = {}
        # protocols
        self._robot_protocol: Optional[RealtimeRobotProtocol] = None
        self._layer_protocol: Optional[LayerProtocol] = None
        # robot protocol
        if robot_protocol is not None:
            self._robot_protocol = robot_protocol
        else:
            self._robot_protocol: RealtimeRobotProtocol = RealtimeRobotProtocol(engine_hostname,
                                                                                auto_commit)
        # layer protocol
        if layer_protocol is not None:
            self._layer_protocol = layer_protocol
        else:
            self._layer_protocol: LayerProtocol = LayerProtocol(engine_hostname, auto_commit)
        # robots by name
        self._robots_makers: Dict[str, Callable[[str, ...], RobotAbs]] = {
            "DB21M": self.DB21M,
            "DB21J": self.DB21J,
            "DBR4": self.DBR4,
            "DB19": self.DB19,
            "DB18": self.DB18,
            "WT21A": self.WT21A,
            "WT21B": self.WT21B,
            "WT19A": self.WT19A,
            "WT19B": self.WT19B,
            "WT18": self.WT18,
            "DC21": self.DC21,
        }
        # ---
        self._lock = Semaphore()

    def _add(self, key: str, robot: RobotAbs):
        # add new robot
        with self._lock:
            self._robots[key] = robot

    def _make_pose(self, key: str, **kwargs) -> Pose3D:
        return Pose3D(self._layer_protocol, key, **kwargs)

    def _make_robot(self, key: str, factory: Type[T], features: Set[RobotFeature],
                    raw_pose: bool = False, **kwargs) -> T:
        # expose raw 'frames' layer
        if raw_pose:
            features.add(RobotFeature.FRAME)
        robot = factory(self._robot_protocol, key, features, self._layer_protocol, **kwargs)
        # add robot
        self._add(key, robot)
        # ---
        return robot

    def create(self, model: str, key: str, **kwargs):
        if model not in self._robots_makers:
            raise ValueError(f"Model '{model}' not recognized.")
        maker = self._robots_makers[model]
        return maker(key, **kwargs)

    def DB21M(self, key: str, **kwargs) -> DB21M:
        features: Set[RobotFeature] = {
            RobotFeature.DIFFERENTIAL_DRIVE,
            RobotFeature.CAMERA_0,
            RobotFeature.ENCODER_LEFT,
            RobotFeature.ENCODER_RIGHT,
            RobotFeature.TOF_FRONT_CENTER,
            RobotFeature.LIGHTS_5,
        }
        return self._make_robot(key, DB21M, features, **kwargs)

    def DB21J(self, key: str, **kwargs) -> DB21J:
        features: Set[RobotFeature] = {
            RobotFeature.DIFFERENTIAL_DRIVE,
            RobotFeature.CAMERA_0,
            RobotFeature.ENCODER_LEFT,
            RobotFeature.ENCODER_RIGHT,
            RobotFeature.TOF_FRONT_CENTER,
            RobotFeature.LIGHTS_5,
        }
        return self._make_robot(key, DB21J, features, **kwargs)

    def DBR4(self, key: str, **kwargs) -> DBR4:
        features: Set[RobotFeature] = {
            RobotFeature.DIFFERENTIAL_DRIVE,
            RobotFeature.CAMERA_0,
            RobotFeature.ENCODER_LEFT,
            RobotFeature.ENCODER_RIGHT,
            RobotFeature.TOF_FRONT_CENTER,
            RobotFeature.LIGHTS_5,
        }
        return self._make_robot(key, DBR4, features, **kwargs)

    def DB19(self, key: str, **kwargs) -> DB19:
        features: Set[RobotFeature] = {
            RobotFeature.DIFFERENTIAL_DRIVE,
            RobotFeature.CAMERA_0,
            RobotFeature.ENCODER_LEFT,
            RobotFeature.ENCODER_RIGHT,
            RobotFeature.LIGHTS_5,
        }
        return self._make_robot(key, DB19, features, **kwargs)

    def DB18(self, key: str, **kwargs) -> DB18:
        features: Set[RobotFeature] = {
            RobotFeature.DIFFERENTIAL_DRIVE,
            RobotFeature.CAMERA_0,
            RobotFeature.LIGHTS_5,
        }
        return self._make_robot(key, DB18, features, **kwargs)

    def WT21A(self, key: str, **kwargs) -> WT21A:
        features: Set[RobotFeature] = {
            RobotFeature.CAMERA_0
        }
        return self._make_robot(key, WT21A, features, **kwargs)

    def WT21B(self, key: str, **kwargs) -> WT21B:
        features: Set[RobotFeature] = {
            RobotFeature.CAMERA_0,
        }
        return self._make_robot(key, WT21B, features, **kwargs)

    def WT19A(self, key: str, **kwargs) -> WT19A:
        features: Set[RobotFeature] = {
            RobotFeature.CAMERA_0,
        }
        return self._make_robot(key, WT19A, features, **kwargs)

    def WT19B(self, key: str, **kwargs) -> WT19B:
        features: Set[RobotFeature] = {
            RobotFeature.CAMERA_0,
        }
        return self._make_robot(key, WT19B, features, **kwargs)

    def WT18(self, key: str, **kwargs) -> WT18:
        features: Set[RobotFeature] = {
            RobotFeature.CAMERA_0,
        }
        return self._make_robot(key, WT18, features, **kwargs)

    def DC21(self, key: str, **kwargs) -> DC21:
        features: Set[RobotFeature] = {
            RobotFeature.CAMERA_0,
        }
        return self._make_robot(key, DC21, features, **kwargs)

    # Generic Types

    def CameraEnabledRobot(self, key: str, **kwargs) -> CameraEnabledRobot:
        features: Set[RobotFeature] = {
            RobotFeature.CAMERA_0,
        }
        return self._make_robot(key, CameraEnabledRobot, features, **kwargs)

    def WheeledRobot(self, key: str, encoders: bool, **kwargs) -> WheeledRobot:
        features: Set[RobotFeature] = {
            RobotFeature.DIFFERENTIAL_DRIVE,
        }
        if encoders:
            features.update({
                RobotFeature.ENCODER_LEFT,
                RobotFeature.ENCODER_RIGHT,
            })
        return self._make_robot(key, WheeledRobot, features, **kwargs)

    def LightsEnabledRobot(self, key: str, **kwargs) -> LightsEnabledRobot:
        features: Set[RobotFeature] = {
            RobotFeature.LIGHTS_5,
        }
        return self._make_robot(key, LightsEnabledRobot, features, **kwargs)

    def RangeEnabledRobot(self, key: str, **kwargs) -> RangeEnabledRobot:
        features: Set[RobotFeature] = {
            RobotFeature.TOF_FRONT_CENTER,
        }
        return self._make_robot(key, RangeEnabledRobot, features, **kwargs)
