from threading import Semaphore
from typing import Dict, TypeVar, Type, Optional

import numpy as np

from dt_duckiematrix_protocols.commons.LayerProtocol import LayerProtocol
from dt_duckiematrix_protocols.commons.ProtocolAbs import ProtocolAbs
from dt_duckiematrix_protocols.types.colors import IColor, LocalColor
from dt_duckiematrix_protocols.types.geometry import LocalVector3, IVector3, LocalPose3D, IPose3D
from dt_duckiematrix_protocols.types.markers import IMarker
from dt_duckiematrix_protocols.viewer.markers import \
    MarkerAbs, \
    MarkerAction, \
    MarkerCube, \
    MarkerSphere, \
    MarkerCylinder, \
    MarkerQuad, \
    MarkerArrow, \
    MarkerText, \
    MarkerTrajectory, \
    MarkerSimple, \
    MarkerMultipart, \
    MarkerCone

T = TypeVar('T')


class MarkersManager:

    def __init__(self, engine_hostname: str, auto_commit: bool = False,
                 layer_protocol: Optional[LayerProtocol] = None):
        self._markers: Dict[str, IMarker] = {}
        self._markers_actions: Dict[str, MarkerAction] = {}

        # protocols
        self._layer_protocol: Optional[LayerProtocol] = None
        if layer_protocol is not None:
            self._layer_protocol = layer_protocol
        else:
            self._layer_protocol: LayerProtocol = LayerProtocol(engine_hostname, auto_commit)

        self._auto_commit = auto_commit
        self._lock = Semaphore(1)

    def session(self) -> ProtocolAbs.SessionProtocolContext:
        return self._layer_protocol.session()

    def atomic(self) -> ProtocolAbs.AtomicProtocolContext:
        return self._layer_protocol.atomic()

    def _add(self, key: str, marker: IMarker):
        # TODO: not sure what happens when markers are replaced with different types
        # issue a REMOVE action when another marker with the same key already exists
        if key in self._markers:
            self._remove(key)
        # add new marker
        with self._lock:
            if isinstance(marker, MarkerSimple):
                self._markers[key] = marker
                self._markers_actions[key] = MarkerAction.ADD_OR_UPDATE
                self._layer_protocol.update("markers", key, marker.as_dict())
            elif isinstance(marker, MarkerMultipart):
                for k, m in marker.as_dict().items():
                    self._markers[k] = m
                    self._markers_actions[k] = MarkerAction.ADD_OR_UPDATE
                    self._layer_protocol.update("markers", k, m)
            else:
                raise ValueError(f"Marker of type {type(marker).__name__} not recognized.")

    def _remove(self, key: str):
        with self._lock:
            marker = self._markers.pop(key, None)
            if marker is None:
                return
            # a marker with the given key existed, propagate a remove
            self._markers_actions[key] = MarkerAction.REMOVE
            self._layer_protocol.update("markers", key, marker.as_dict())

    @staticmethod
    def _make_pose(**kwargs) -> IPose3D:
        return LocalPose3D(**kwargs)

    @staticmethod
    def _make_scale(**kwargs) -> Optional[IVector3]:
        scale_vector = None
        if "scale" in kwargs:
            scale = kwargs["scale"]
            if isinstance(scale, (float, int)):
                scale_vector = [float(scale), float(scale), float(scale)]
            elif isinstance(scale, np.ndarray):
                if scale.shape != (3,):
                    raise ValueError(f"Object '{scale}' is not a valid scale.")
                scale_vector = scale.astype(np.float).tolist()
            elif isinstance(scale, (list, tuple)):
                if len(scale) != 3:
                    raise ValueError(f"Object '{scale}' is not a valid scale.")
                scale_vector = list(map(float, scale))
            else:
                raise ValueError(f"Object '{scale}' is not a valid scale.")
        if scale_vector is not None:
            data = dict(zip(["x", "y", "z"], scale_vector))
            return LocalVector3(**data)

    @staticmethod
    def _make_color(**kwargs) -> Optional[IColor]:
        color_vector = None
        if "color" in kwargs:
            color = kwargs["color"]
            if isinstance(color, (float, int)):
                color_vector = [float(color), float(color), float(color)]
            elif isinstance(color, np.ndarray):
                if color.shape != (3,) and color.shape != (4,):
                    raise ValueError(f"Object '{color}' is not a valid color.")
                color_vector = color.astype(np.float).tolist()
            elif isinstance(color, (list, tuple)):
                if len(color) != 3 and len(color) != 4:
                    raise ValueError(f"Object '{color}' is not a valid color.")
                color_vector = list(map(float, color))
            else:
                raise ValueError(f"Object '{color}' is not a valid color.")
        if color_vector is not None and len(color_vector) == 3:
            color_vector = color_vector + [1.0]
        if color_vector is not None:
            data = dict(zip(["r", "g", "b", "a"], color_vector))
            return LocalColor(**data)

    def _make_marker(self, key: str, factory: Type[T], **kwargs) -> T:
        auto_commit: bool = self._auto_commit
        with self._layer_protocol.atomic():
            marker: MarkerAbs = factory(self._layer_protocol, key, auto_commit, **kwargs)
            # pose
            pose = self._make_pose(**kwargs)
            marker.pose.update(pose)
            # scale
            scale = self._make_scale(**kwargs)
            if scale is not None:
                marker.scale.update(scale)
            # color
            color = self._make_color(**kwargs)
            if color is not None:
                marker.color.update(color)
            # action
            marker.action = MarkerAction.ADD_OR_UPDATE
            # add marker
            self._add(key, marker)
        # ---
        return marker

    def Cube(self, key: str, **kwargs) -> MarkerCube:
        return self._make_marker(key, MarkerCube, **kwargs)

    def Sphere(self, key: str, **kwargs) -> MarkerSphere:
        return self._make_marker(key, MarkerSphere, **kwargs)

    def Cylinder(self, key: str, **kwargs) -> MarkerCylinder:
        return self._make_marker(key, MarkerCylinder, **kwargs)

    def Quad(self, key: str, **kwargs) -> MarkerQuad:
        return self._make_marker(key, MarkerQuad, **kwargs)

    def Cone(self, key: str, **kwargs) -> MarkerCone:
        return self._make_marker(key, MarkerCone, **kwargs)

    def Arrow(self, key: str, **kwargs) -> MarkerArrow:
        return self._make_marker(key, MarkerArrow, **kwargs)

    def Text(self, key: str, **kwargs) -> MarkerText:
        return self._make_marker(key, MarkerText, **kwargs)
        # TODO: add custom fields setup

    def Trajectory(self, key: str, **kwargs) -> MarkerTrajectory:
        return self._make_marker(key, MarkerTrajectory, **kwargs)
        # TODO: add custom fields setup
