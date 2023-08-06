from abc import abstractmethod, ABC
from enum import IntEnum
from typing import Union

from dt_duckiematrix_protocols.types.colors import IColor
from dt_duckiematrix_protocols.types.geometry import IPose3D, IVector3


class MarkerType(IntEnum):
    CUBE = 0
    SPHERE = 1
    CYLINDER = 2
    QUAD = 3
    CONE = 4
    TEXT = 5
    TRAJECTORY = 6

    @staticmethod
    def get_class(marker_type: 'MarkerType'):
        from dt_duckiematrix_protocols.viewer import MarkerCube, MarkerSphere, MarkerCylinder, \
            MarkerQuad, MarkerCone, MarkerText, MarkerTrajectory
        return {
            MarkerType.CUBE: MarkerCube,
            MarkerType.SPHERE: MarkerSphere,
            MarkerType.CYLINDER: MarkerCylinder,
            MarkerType.QUAD: MarkerQuad,
            MarkerType.CONE: MarkerCone,
            MarkerType.TEXT: MarkerText,
            MarkerType.TRAJECTORY: MarkerTrajectory,
        }[marker_type]


class MarkerAction(IntEnum):
    ADD_OR_UPDATE = 0
    REMOVE = 1
    HIDE = 2
    SHOW = 3


class IMarker(ABC):

    @property
    @abstractmethod
    def type(self) -> MarkerType:
        pass

    @property
    @abstractmethod
    def pose(self) -> IPose3D:
        pass

    @pose.setter
    @abstractmethod
    def pose(self, value: IPose3D):
        pass

    @property
    @abstractmethod
    def scale(self) -> IVector3:
        pass

    @scale.setter
    @abstractmethod
    def scale(self, value: Union[int, float, IVector3]):
        pass

    @property
    @abstractmethod
    def color(self) -> IColor:
        pass

    @color.setter
    @abstractmethod
    def color(self, value: Union[int, float, IColor]):
        pass

    @abstractmethod
    def show(self):
        pass

    @abstractmethod
    def hide(self):
        pass

    @abstractmethod
    def destroy(self):
        pass

    @abstractmethod
    def as_dict(self) -> dict:
        pass
