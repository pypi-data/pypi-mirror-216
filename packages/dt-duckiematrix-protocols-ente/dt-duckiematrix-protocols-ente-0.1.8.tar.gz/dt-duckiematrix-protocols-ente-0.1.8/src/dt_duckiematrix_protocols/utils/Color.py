import abc

from dt_duckiematrix_protocols.commons.LayerProtocol import LayerProtocol
from dt_duckiematrix_protocols.types.colors import IColor
from dt_duckiematrix_protocols.utils.MonitoredObject import MonitoredObject


class Color(MonitoredObject, IColor):

    EMPTY_DICT = {}

    def __init__(self, layers: LayerProtocol, key: str, auto_commit: bool = False, **kwargs):
        super().__init__(auto_commit)
        self._layers = layers
        self._key = key
        # ensure the layer struct is there
        self._make_layers()
        # update with given attrs
        with self.quiet():
            for k in self.COLOR_ATTRS:
                if k in kwargs:
                    self._set_property(k, kwargs[k])

    @abc.abstractmethod
    def _make_layers(self):
        pass

    def update(self, other: IColor, quiet: bool = False):
        if not isinstance(other, IColor):
            raise ValueError(f"Expected 'IColor', got '{type(other).__name__}' instead.")
        ctx = self.quiet if quiet else self.atomic
        with ctx():
            for k in self.COLOR_ATTRS:
                self._set_property(k, other._get_property(k))
