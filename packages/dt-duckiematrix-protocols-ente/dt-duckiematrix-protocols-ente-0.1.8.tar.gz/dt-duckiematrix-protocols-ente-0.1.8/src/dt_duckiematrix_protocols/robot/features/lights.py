from typing import Any, Dict, List

from dt_duckiematrix_protocols.commons.LayerProtocol import LayerProtocol
from dt_duckiematrix_protocols.commons.ProtocolAbs import ProtocolAbs
from dt_duckiematrix_protocols.utils.Color import Color
from dt_duckiematrix_protocols.utils.types import sanitize_color_float


class HexColor(Color):
    DEFAULT_COLOR = "#fff"

    def __init__(self, layers: LayerProtocol, layer: str, key: str, auto_commit: bool = False, **kwargs):
        self._layer: str = layer
        self._color: Dict[str, float] = {
            "r": 1.0,
            "g": 1.0,
            "b": 1.0,
            "a": 1.0,
        }
        super(HexColor, self).__init__(layers=layers, key=key, auto_commit=auto_commit, **kwargs)

    def _make_layers(self):
        self._layers.set_quiet(self._layer, self._key, "color", self.DEFAULT_COLOR)

    def _get_property(self, field: str) -> float:
        return self._color[field]

    def _set_property(self, field: str, value: Any, quiet: bool = False):
        value: float = sanitize_color_float(field, value)
        self._color[field] = value
        self._commit()
        if self._auto_commit and not quiet:
            self._commit()

    def _commit(self):
        entity = self._layers.get(self._layer, self._key)
        entity["color"] = self._rgb_to_hex(**self._color)
        entity["intensity"] = self._color["a"]
        self._layers.update(self._layer, self._key, entity)

    @staticmethod
    def _rgb_to_hex(r: float, g: float, b: float, **_):
        return '#{:02x}{:02x}{:02x}ff'.format(int(r * 255), int(g * 255), int(b * 255))


class LED:

    def __init__(self, protocol: LayerProtocol, key: str, auto_commit: bool = False):
        self._protocol: LayerProtocol = protocol
        self._key: str = key
        self._color = HexColor(protocol, "lights", self._key, auto_commit)

    @property
    def color(self) -> HexColor:
        return self._color


class Lights:
    """
    Duckiebots have 5 LEDs that are indexed and positioned as following:

    +------------------+------------------------------------------+
    | Index            | Position (rel. to direction of movement) |
    +==================+==========================================+
    | 0                | Front left                               |
    +------------------+------------------------------------------+
    | 1                | Rear left                                |
    +------------------+------------------------------------------+
    | 2                | Top / Front middle                       |
    +------------------+------------------------------------------+
    | 3                | Rear right                               |
    +------------------+------------------------------------------+
    | 4                | Front right                              |
    +------------------+------------------------------------------+

    """

    def __init__(self, protocol: LayerProtocol, key: str, auto_commit: bool = False):
        self._protocol: LayerProtocol = protocol
        self._key: str = key
        self._auto_commit: bool = auto_commit
        self._leds: Dict[int, LED] = {
            i: LED(self._protocol, f"{self._key}/light_{i}", self._auto_commit)
            for i in range(5)
        }
        self._all = LED(self._protocol, f"{self._key}", self._auto_commit)

    def session(self) -> ProtocolAbs.SessionProtocolContext:
        return self._protocol.session()

    def atomic(self) -> ProtocolAbs.AtomicProtocolContext:
        return ProtocolAbs.AtomicProtocolContext(self._protocol)

    @property
    def all(self) -> LED:
        return self._all

    @property
    def light0(self) -> LED:
        return self._leds[0]

    @property
    def light1(self) -> LED:
        return self._leds[1]

    @property
    def light2(self) -> LED:
        return self._leds[2]

    @property
    def light3(self) -> LED:
        return self._leds[3]

    @property
    def light4(self) -> LED:
        return self._leds[4]
