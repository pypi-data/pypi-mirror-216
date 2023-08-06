from abc import ABC, abstractmethod
from typing import Dict


class IColor(ABC):

    COLOR_ATTRS = ["r", "g", "b", "a"]

    @abstractmethod
    def _get_property(self, field: str) -> float:
        pass

    @abstractmethod
    def _set_property(self, field: str, value: float, quiet: bool = False):
        pass

    @property
    def r(self) -> float:
        return self._get_property("r")

    @r.setter
    def r(self, value):
        self._set_property("r", value)

    @property
    def g(self) -> float:
        return self._get_property("g")

    @g.setter
    def g(self, value):
        self._set_property("g", value)

    @property
    def b(self) -> float:
        return self._get_property("b")

    @b.setter
    def b(self, value):
        self._set_property("b", value)

    @property
    def a(self) -> float:
        return self._get_property("a")

    @a.setter
    def a(self, value):
        self._set_property("a", value)

    def update_quiet(self, other: 'IColor'):
        self.update(other, quiet=True)

    def update(self, other: 'IColor', quiet: bool = False):
        if not isinstance(other, IColor):
            raise ValueError(f"Expected 'IColor', got '{type(other).__name__}' instead.")
        for k in self.COLOR_ATTRS:
            self._set_property(k, other._get_property(k), quiet=quiet)

    def __str__(self):
        return str({k: self._get_property(k) for k in self.COLOR_ATTRS})


class LocalColor(IColor):

    def __init__(self, **kwargs):
        self._data: Dict[str, float] = {}
        # set values
        for k in self.COLOR_ATTRS:
            self._set_property(k, kwargs.get(k, 1.0), quiet=True)

    def _get_property(self, field: str) -> float:
        return self._data[field]

    def _set_property(self, field: str, value: float, quiet: bool = False):
        self._data[field] = value
