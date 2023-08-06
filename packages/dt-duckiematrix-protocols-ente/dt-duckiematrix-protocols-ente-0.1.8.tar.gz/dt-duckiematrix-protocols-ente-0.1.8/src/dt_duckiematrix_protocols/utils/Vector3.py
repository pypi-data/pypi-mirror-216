import abc

from dt_duckiematrix_protocols.commons.LayerProtocol import LayerProtocol
from dt_duckiematrix_protocols.types.geometry import IVector3
from dt_duckiematrix_protocols.utils.MonitoredObject import MonitoredObject


class Vector3(MonitoredObject, IVector3):

    EMPTY_DICT = {}

    def __init__(self, layers: LayerProtocol, key: str, auto_commit: bool = False, **kwargs):
        super().__init__(auto_commit)
        self._layers = layers
        self._key = key
        self._atomic = False
        # ensure the layer struct is there
        self._make_layers()
        # update with given attrs
        with self.quiet():
            for k in self.VECTOR3_ATTRS:
                if k in kwargs:
                    self._set_property(k, kwargs[k])

    @abc.abstractmethod
    def _make_layers(self):
        pass

    def update(self, other: IVector3, quiet: bool = False):
        if not isinstance(other, IVector3):
            raise ValueError(f"Expected 'IVector3', got '{type(other).__name__}' instead.")
        ctx = self.quiet if quiet else self.atomic
        with ctx():
            for k in self.VECTOR3_ATTRS:
                self._set_property(k, other._get_property(k))
