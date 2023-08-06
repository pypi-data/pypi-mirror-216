from abc import abstractmethod, ABC
from typing import Union, Optional, Dict

import numpy as np

from dt_duckiematrix_protocols.utils.types import sanitize_float

IPoint3D = Union[list, np.ndarray]


class IPose3D(ABC):

    POSE_ATTRS = ["x", "y", "z", "roll", "pitch", "yaw"]

    @abstractmethod
    def _get_property(self, field: str) -> float:
        pass

    @abstractmethod
    def _set_property(self, field: str, value: float, quiet: bool = False):
        pass

    @property
    @abstractmethod
    def relative_to(self) -> Optional[str]:
        pass

    @relative_to.setter
    @abstractmethod
    def relative_to(self, value: Optional[str]):
        pass

    @property
    def x(self) -> float:
        return self._get_property("x")

    @x.setter
    def x(self, value):
        self._set_property("x", value)

    @property
    def y(self) -> float:
        return self._get_property("y")

    @y.setter
    def y(self, value):
        self._set_property("y", value)

    @property
    def z(self) -> float:
        return self._get_property("z")

    @z.setter
    def z(self, value):
        self._set_property("z", value)

    @property
    def roll(self) -> float:
        return self._get_property("roll")

    @roll.setter
    def roll(self, value):
        self._set_property("roll", value)

    @property
    def pitch(self) -> float:
        return self._get_property("pitch")

    @pitch.setter
    def pitch(self, value):
        self._set_property("pitch", value)

    @property
    def yaw(self) -> float:
        return self._get_property("yaw")

    @yaw.setter
    def yaw(self, value):
        self._set_property("yaw", value)

    def update_quiet(self, other: 'IPose3D'):
        self.update(other, quiet=True)

    def update(self, other: 'IPose3D', quiet: bool = False):
        if not isinstance(other, IPose3D):
            raise ValueError(f"Expected 'IPose3D', got '{type(other).__name__}' instead.")
        for k in self.POSE_ATTRS:
            self._set_property(k, other._get_property(k), quiet=quiet)

    def __str__(self):
        return str({
            "relative_to": self.relative_to,
            "pose": {k: self._get_property(k) for k in self.POSE_ATTRS}
        })


class IVector3(ABC):

    VECTOR3_ATTRS = ["x", "y", "z"]

    @abstractmethod
    def _get_property(self, field: str) -> float:
        pass

    @abstractmethod
    def _set_property(self, field: str, value: float, quiet: bool = False):
        pass

    @property
    def x(self) -> float:
        return self._get_property("x")

    @x.setter
    def x(self, value: float):
        self._set_property("x", value)

    @property
    def y(self) -> float:
        return self._get_property("y")

    @y.setter
    def y(self, value: float):
        self._set_property("y", value)

    @property
    def z(self) -> float:
        return self._get_property("z")

    @z.setter
    def z(self, value: float):
        self._set_property("z", value)

    def update_quiet(self, other: 'IVector3'):
        self.update(other, quiet=True)

    def update(self, other: 'IVector3', quiet: bool = False):
        if not isinstance(other, IVector3):
            raise ValueError(f"Expected 'IVector3', got '{type(other).__name__}' instead.")
        for k in self.VECTOR3_ATTRS:
            self._set_property(k, other._get_property(k), quiet=quiet)

    def __str__(self):
        return str({k: self._get_property(k) for k in self.VECTOR3_ATTRS})


class LocalPose3D(IPose3D):

    def __init__(self, **kwargs):
        self._pose: Dict[str, float] = {}
        self._relative_to: Optional[str] = kwargs.get("relative_to", None)
        # set values
        for k in self.POSE_ATTRS:
            v = sanitize_float(k, kwargs.get(k, 0.0))
            self._set_property(k, v, quiet=True)

    def _get_property(self, field: str) -> float:
        return self._pose[field]

    def _set_property(self, field: str, value: float, quiet: bool = False):
        self._pose[field] = value

    @property
    def relative_to(self) -> Optional[str]:
        return self._relative_to

    @relative_to.setter
    def relative_to(self, value: Optional[str]):
        self._relative_to = value


class LocalVector3(IVector3):

    def __init__(self, **kwargs):
        self._data: Dict[str, float] = {}
        # set values
        for k in self.VECTOR3_ATTRS:
            self._set_property(k, kwargs.get(k, 0.0), quiet=True)

    def _get_property(self, field: str) -> float:
        return self._data[field]

    def _set_property(self, field: str, value: float, quiet: bool = False):
        self._data[field] = value
