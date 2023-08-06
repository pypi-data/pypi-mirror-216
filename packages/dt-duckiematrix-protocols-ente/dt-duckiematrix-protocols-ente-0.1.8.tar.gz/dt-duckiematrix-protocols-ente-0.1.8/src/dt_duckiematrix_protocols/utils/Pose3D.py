from typing import Any, Optional

import numpy as np

from dt_duckiematrix_protocols.commons.LayerProtocol import LayerProtocol
from dt_duckiematrix_protocols.types.geometry import IPose3D
from dt_duckiematrix_protocols.utils.MonitoredObject import MonitoredObject

BUILTIN_TYPES = (
    int,
    float,
    bool,
    str,
    list,
    tuple,
    dict,
    set,
    frozenset,
)


class Pose3D(MonitoredObject, IPose3D):

    EMPTY_DICT = {}

    def __init__(self, layers: LayerProtocol, key: str, auto_commit: bool = False, **kwargs):
        super(Pose3D, self).__init__(auto_commit)
        self._layers = layers
        self._key = key
        # make frame if it does not exist
        if not self._layers.has("frames", self._key):
            self._layers.update_quiet("frames", self._key, {
                "relative_to": None,
                "pose": {k: 0.0 for k in self.POSE_ATTRS}
            })
        # update with given attrs
        if "relative_to" in kwargs:
            self.relative_to = kwargs["relative_to"]
        with self.quiet():
            for k in self.POSE_ATTRS:
                if k in kwargs:
                    self._set_property(k, kwargs[k])

    def _get_property(self, field: str) -> float:
        return self._layers.get("frames", self._key).get("pose").get(field, None)

    def _set_property(self, field: str, value: Any, quiet: bool = False):
        # make sure the value is YAML-serializable
        if value is not None and value.__class__ not in BUILTIN_TYPES:
            # Numpy float values
            if isinstance(value, (np.float32, np.float64)):
                value = float(value)
            # Numpy int values
            elif isinstance(value, (np.int8, np.int16, np.int32, np.int64, np.uint)):
                value = int(value)
            # unknown value
            else:
                self._layers.logger.error(f"You cannot set the property '{field}' to an object "
                                          f"of type '{type(value)}'")
                return
        pose = self._layers.get("frames", self._key)
        pose["pose"][field] = value
        if self._auto_commit and not quiet:
            self._commit()

    def _commit(self):
        pose = self._layers.get("frames", self._key)
        self._layers.update("frames", self._key, pose)

    @property
    def relative_to(self) -> Optional[str]:
        return self._layers.get("frames", self._key).get("relative_to")

    @relative_to.setter
    def relative_to(self, value):
        self._layers.get("frames", self._key)["relative_to"] = value

    def update(self, other: IPose3D, quiet: bool = False):
        if not isinstance(other, IPose3D):
            raise ValueError(f"Expected 'IPose3D', got '{type(other).__name__}' instead.")
        ctx = self.quiet if quiet else self.atomic
        with ctx():
            for k in self.POSE_ATTRS:
                self._set_property(k, other._get_property(k))
