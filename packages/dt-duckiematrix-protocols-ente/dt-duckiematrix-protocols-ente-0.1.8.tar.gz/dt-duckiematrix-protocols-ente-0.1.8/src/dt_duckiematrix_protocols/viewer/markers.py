import os
from abc import abstractmethod, ABC
from typing import Any, Union

import numpy as np

from dt_duckiematrix_messages import CBorMessage
from dt_duckiematrix_protocols.commons.LayerProtocol import LayerProtocol
from dt_duckiematrix_protocols.types.colors import IColor, LocalColor
from dt_duckiematrix_protocols.types.geometry import \
    IPoint3D, \
    IPose3D, \
    IVector3, \
    LocalPose3D, \
    LocalVector3
from dt_duckiematrix_protocols.types.markers import IMarker, MarkerAction, MarkerType
from dt_duckiematrix_protocols.utils.Color import Color
from dt_duckiematrix_protocols.utils.MonitoredObject import MonitoredObject
from dt_duckiematrix_protocols.utils.Pose3D import Pose3D
from dt_duckiematrix_protocols.utils.Vector3 import Vector3
from dt_duckiematrix_protocols.utils.types import sanitize_float, sanitize_color_float


class MarkerScale(Vector3):

    def _make_layers(self):
        self._layers.set_quiet("markers", self._key, "scale", {})

    def _get_property(self, field: str) -> float:
        return self._layers.get("markers", self._key).get("scale").get(field, None)

    def _set_property(self, field: str, value: Any, quiet: bool = False):
        value = sanitize_float(field, value)
        marker = self._layers.get("markers", self._key)
        marker["scale"][field] = value
        if self._auto_commit and not quiet:
            self._commit()

    def _commit(self):
        marker = self._layers.get("markers", self._key)
        self._layers.update("markers", self._key, marker)


class MarkerColor(Color):

    def _make_layers(self):
        self._layers.set_quiet("markers", self._key, "color", {})

    def _get_property(self, field: str) -> float:
        return self._layers.get("markers", self._key).get("color").get(field, None)

    def _set_property(self, field: str, value: Any, quiet: bool = False):
        value = sanitize_color_float(field, value)
        marker = self._layers.get("markers", self._key)
        marker["color"][field] = value
        if self._auto_commit and not quiet:
            self._commit()

    def _commit(self):
        marker = self._layers.get("markers", self._key)
        self._layers.update("markers", self._key, marker)


class MarkerAbs(MonitoredObject, CBorMessage, IMarker):

    def __init__(self, layers: LayerProtocol, key: str, auto_commit: bool = False, **_):
        super().__init__(auto_commit)
        self._key = key
        self._layers = layers
        # fields
        with layers.session():
            self._pose: Pose3D = Pose3D(layers, key,
                                        auto_commit=auto_commit)
            self._scale: Vector3 = MarkerScale(layers, key,
                                               auto_commit=auto_commit,
                                               x=1.0, y=1.0, z=1.0)
            self._color: Color = MarkerColor(layers, key,
                                             auto_commit=auto_commit,
                                             r=1.0, g=1.0, b=1.0, a=1.0)
        self._action: MarkerAction = MarkerAction.ADD_OR_UPDATE
        # ---
        self._layers.set_quiet("markers", self._key, "type", self.type)
        self._layers.set_quiet("markers", self._key, "action", self._action)
        # commit
        if auto_commit:
            self._commit()

    def _commit(self):
        with self._layers.session():
            self._pose.commit()
            self._layers.update("markers", self._key, self.as_dict())

    @property
    @abstractmethod
    def type(self) -> MarkerType:
        pass

    @property
    def pose(self) -> IPose3D:
        return self._pose

    @pose.setter
    def pose(self, value: IPose3D):
        if isinstance(value, IPose3D):
            with self._pose.atomic():
                self._pose.x = value.x
                self._pose.y = value.y
                self._pose.z = value.z
                self._pose.roll = value.roll
                self._pose.pitch = value.pitch
                self._pose.yaw = value.yaw
        else:
            raise ValueError(f"You cannot assign object of type '{type(value).__name__}' to "
                             f"field 'pose'. Expected 'IPose3D'.")

    @property
    def scale(self) -> IVector3:
        return self._scale

    @scale.setter
    def scale(self, value: Union[int, float, IVector3]):
        if isinstance(value, (float, int)):
            value = float(value)
            with self._scale.atomic():
                self._scale.x = value
                self._scale.y = value
                self._scale.z = value
        elif isinstance(value, IVector3):
            with self._scale.atomic():
                self._scale.x = value.x
                self._scale.y = value.y
                self._scale.z = value.z
        else:
            raise ValueError(f"You cannot assign object of type '{type(value).__name__}' to "
                             f"field 'scale'. Expected 'Union[int, float, IVector3]'.")

    @property
    def color(self) -> IColor:
        return self._color

    @color.setter
    def color(self, value: Union[int, float, IColor]):
        if isinstance(value, (int, float)):
            if isinstance(value, int):
                value = value / 255.0
            with self._color.atomic():
                self._color.r = value
                self._color.g = value
                self._color.b = value
        elif isinstance(value, IColor):
            with self._color.atomic():
                self._color.r = value.r
                self._color.g = value.g
                self._color.b = value.b
                self._color.a = value.a

    def show(self):
        self._action = MarkerAction.SHOW
        self._layers.update("markers", self._key, {"action": self._action})

    def hide(self):
        self._action = MarkerAction.HIDE
        self._layers.update("markers", self._key, {"action": self._action})

    def destroy(self):
        self._action = MarkerAction.REMOVE
        self._layers.update("markers", self._key, {"action": self._action})

    def as_dict(self) -> dict:
        return self._layers.get("markers", self._key)


class MarkerSimple(MarkerAbs, ABC):
    pass


class MarkerCube(MarkerSimple):

    @property
    def type(self) -> MarkerType:
        return MarkerType.CUBE


class MarkerSphere(MarkerSimple):

    @property
    def type(self) -> MarkerType:
        return MarkerType.SPHERE


class MarkerCylinder(MarkerSimple):

    @property
    def type(self) -> MarkerType:
        return MarkerType.CYLINDER


class MarkerQuad(MarkerSimple):

    @property
    def type(self) -> MarkerType:
        return MarkerType.QUAD


class MarkerCone(MarkerSimple):

    @property
    def type(self) -> MarkerType:
        return MarkerType.CONE


class MarkerMultipart(IMarker, ABC):
    pass


class MarkerArrow(MarkerMultipart):

    class MarkerArrowPose3D(LocalPose3D):

        def __init__(self, arrow: 'MarkerArrow', auto_commit: bool = False, **kwargs):
            self._arrow = arrow
            self._auto_commit = auto_commit
            super(MarkerArrow.MarkerArrowPose3D, self).__init__(**kwargs)

        def _set_property(self, field: str, value: float, quiet: bool = False):
            super(MarkerArrow.MarkerArrowPose3D, self)._set_property(field, value)
            if not quiet:
                self._arrow._recompute_arrow_parts()

    class MarkerArrowVector3(LocalVector3):

        def __init__(self, arrow: 'MarkerArrow', auto_commit: bool = False, **kwargs):
            self._arrow = arrow
            self._auto_commit = auto_commit
            super(MarkerArrow.MarkerArrowVector3, self).__init__(**kwargs)

        def _set_property(self, field: str, value: float, quiet: bool = False):
            super(MarkerArrow.MarkerArrowVector3, self)._set_property(field, value)
            if not quiet:
                self._arrow._recompute_arrow_parts()

    class MarkerArrowColor(LocalColor):

        def __init__(self, arrow: 'MarkerArrow', auto_commit: bool = False, **kwargs):
            self._arrow = arrow
            self._auto_commit = auto_commit
            super(MarkerArrow.MarkerArrowColor, self).__init__(**kwargs)

        def _set_property(self, field: str, value: float, quiet: bool = False):
            super(MarkerArrow.MarkerArrowColor, self)._set_property(field, value)
            if not quiet:
                self._arrow._update_arrow_color()

    def __init__(self, layers: LayerProtocol, key: str, auto_commit: bool = False,
                 length: float = 1.0, **kwargs):
        self._layers = layers
        # make keys
        self._key = key
        self._body_key = os.path.join(self._key, "body")
        self._head_key = os.path.join(self._body_key, "head")
        # properties
        self._length = length
        # parts types
        # - body
        self._body_type = MarkerCylinder
        if "body" in kwargs:
            t = kwargs["body"]
            if not isinstance(t, MarkerType):
                raise ValueError(f"Field 'body'. Expected type 'MarkerType', got "
                                 f"'{type(t).__name__}' instead.")
            self._body_type = MarkerType.get_class(t)
        # - head
        self._head_type = MarkerCone
        if "head" in kwargs:
            t = kwargs["head"]
            if not isinstance(t, MarkerType):
                raise ValueError(f"Field 'head'. Expected type 'MarkerType', got "
                                 f"'{type(t).__name__}' instead.")
            self._head_type = MarkerType.get_class(t)
        # make parts
        with layers.session():
            self._base: MarkerCube = MarkerCube(layers, self._key, False)
            self._body: MarkerSimple = self._body_type(layers, self._body_key, False)
            self._head: MarkerSimple = self._head_type(layers, self._head_key, False)
            # chain base -> body -> head
            self._body.pose.relative_to = self._key
            self._head.pose.relative_to = self._body_key
            # make base invisible
            self._base.scale = 0.0
        # create fake pose, color, and scale objects
        self._pose: MarkerArrow.MarkerArrowPose3D = \
            MarkerArrow.MarkerArrowPose3D(self, auto_commit)
        self._color: MarkerArrow.MarkerArrowColor = \
            MarkerArrow.MarkerArrowColor(self, auto_commit)
        self._scale: MarkerArrow.MarkerArrowVector3 = \
            MarkerArrow.MarkerArrowVector3(self, auto_commit)

    @property
    def type(self) -> MarkerType:
        return MarkerType.ARROW

    @property
    def pose(self) -> IPose3D:
        return self._pose

    @property
    def scale(self) -> IVector3:
        return self._scale

    @property
    def color(self) -> IColor:
        return self._color

    @pose.setter
    def pose(self, value: IPose3D):
        if isinstance(value, IPose3D):
            self._pose.update(value)
            self._recompute_arrow_parts()
        else:
            raise ValueError(f"You cannot assign object of type '{type(value).__name__}' to "
                             f"field 'pose'. Expected 'IPose3D'.")

    @scale.setter
    def scale(self, value: Union[int, float, IVector3]):
        if isinstance(value, (int, float)):
            value = float(value)
            self._scale.x = value
            self._scale.y = value
            self._scale.z = value
            self._recompute_arrow_parts()
        elif isinstance(value, IVector3):
            self._scale.update(value)
            self._recompute_arrow_parts()
        else:
            raise ValueError(f"You cannot assign object of type '{type(value).__name__}' to "
                             f"field 'scale'. Expected 'Union[int, float, IVector3]'.")

    @color.setter
    def color(self, value: Union[int, float, IColor]):
        if isinstance(value, (int, float)):
            if isinstance(value, int):
                value = value / 255.0
            self._color.r = value
            self._color.g = value
            self._color.b = value
            self._update_arrow_color()
        elif isinstance(value, IColor):
            self._color.update(value)
            self._update_arrow_color()
        else:
            raise ValueError(f"You cannot assign object of type '{type(value).__name__}' to "
                             f"field 'color'. Expected 'Union[int, float, IColor]'.")

    def show(self):
        self._base.show()

    def hide(self):
        self._base.hide()

    def destroy(self):
        self._head.destroy()
        self._body.destroy()
        self._base.destroy()

    def _update_arrow_color(self):
        self._body.color.update(self._color)
        self._head.color.update(self._color)
        # commit
        with self._layers.atomic():
            self._body.commit()
            self._head.commit()

    def _recompute_arrow_parts(self):
        # position and orientation
        self._base.pose.update(self._pose)
        self._base.pose.pitch = np.deg2rad(90) + self._pose.pitch
        # scale - head
        self._head.scale.x = self._scale.x * 2.0
        self._head.scale.y = self._scale.y * 2.0
        self._head.scale.z = 2.0 * max(self._scale.x, self._scale.y)
        # scale - body
        self._body.scale.update(self._scale)
        self._body.scale.z -= self._head.scale.z / 2.0
        # position - body
        self._body.pose.z = self._scale.z - self._head.scale.z / 2.0
        # position - head
        self._head.pose.z = self._body.scale.z + self._head.scale.z / 2.0
        # commit
        with self._layers.atomic():
            self._base.commit()
            self._body.commit()
            self._head.commit()

    def as_dict(self) -> dict:
        return {
            self._key: self._base.as_dict(),
            self._body_key: self._body.as_dict(),
            self._head_key: self._head.as_dict(),
        }

    @classmethod
    def from_two_points(cls, start: IPoint3D, end: IPoint3D) -> 'MarkerArrow':
        # # TODO
        # ux, uy, uz = start
        # vx, vy, vz = end
        # # compute arrow length
        # d = np.linalg.norm([ux - vx, uy - vy, uz - vz]) / 2.0
        # # compute arrow center
        # cx = (ux + vx) / 2
        # cy = (uy + vy) / 2
        # cz = (uz + vz) / 2
        # # rotate body
        # pitch = np.arcsin(vz - uz)
        # yaw = np.arctan2(vy - uy, vx - ux)
        # # prevent user from setting the position
        # kwargs.pop("x", None)
        # kwargs.pop("y", None)
        # kwargs.pop("z", None)
        # scale = kwargs.pop("scale", 0.01)
        # # make arrow body
        # body = self.Cylinder(f"{key}/body", x=cx, y=cy, z=cz,
        #                      scale=scale, pitch=pitch, yaw=yaw, **kwargs)
        # # TODO: add Cone marker as arrow's head
        pass


class MarkerText(MarkerAbs):

    @property
    def type(self) -> MarkerType:
        return MarkerType.TEXT

    def __init__(self, layers, key: str):
        super(MarkerText, self).__init__(layers, key)
        self._text: str = "text"

    @property
    def text(self) -> str:
        return self._text


class MarkerTrajectory(MarkerAbs):

    @property
    def type(self) -> MarkerType:
        return MarkerType.TRAJECTORY

    def __init__(self, layers, key: str):
        super(MarkerTrajectory, self).__init__(layers, key)
        # TODO
        # self._points: List[Vector3] = None

    # @property
    # def points(self) -> List[Vector3]:
    #     return self._points


__all__ = [
    MarkerCube,
    MarkerSphere,
    MarkerCylinder,
    MarkerQuad,
    MarkerArrow,
    MarkerText,
    MarkerTrajectory,
]
