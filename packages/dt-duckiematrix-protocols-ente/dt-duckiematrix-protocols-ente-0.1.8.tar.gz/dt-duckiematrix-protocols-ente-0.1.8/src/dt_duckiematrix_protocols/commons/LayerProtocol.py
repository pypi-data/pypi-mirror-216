from collections import defaultdict
from threading import Semaphore
from typing import Dict, Set, Any

from dt_duckiematrix_messages.LayerMessage import LayerMessage
from dt_duckiematrix_protocols.commons.ProtocolAbs import ProtocolAbs
from dt_duckiematrix_types import EngineMode


class LayerProtocol(ProtocolAbs):

    def __init__(self, engine_hostname: str, auto_commit: bool = False):
        super(LayerProtocol, self).__init__(engine_hostname, "layer", auto_commit)
        self._layers: Dict[str, Dict[str, dict]] = defaultdict(dict)
        self._layers_updates: Dict[str, Set[str]] = defaultdict(set)
        self._lock = Semaphore(1)

    def has(self, layer: str, key: str):
        return key in self._layers[layer]

    def get(self, layer: str, key: str) -> dict:
        return self._layers[layer].get(key, None)

    def set_quiet(self, layer: str, key: str, field: str, data: Any):
        with self._lock:
            if key not in self._layers[layer]:
                self._layers[layer][key] = {}
            self._layers[layer][key][field] = data
            self._layers_updates[layer].add(key)

    def update_quiet(self, layer: str, key: str, data: dict):
        self.update(layer, key, data, quiet=True)

    def update(self, layer: str, key: str, data: dict, quiet: bool = False):
        with self._lock:
            if key not in self._layers[layer]:
                self._layers[layer][key] = {}
            self._layers[layer][key].update(data)
            self._layers_updates[layer].add(key)
            # auto-commit?
            if self._auto_commit and not quiet:
                self.commit(lock=False)

    def commit(self, lock: bool = True):
        if lock:
            self._lock.acquire()
        # ---
        for layer, keys in self._layers_updates.items():
            content = {
                key: self._layers[layer][key]
                for key in keys
            }
            msg = LayerMessage(content)
            self._socket.publish(layer, msg)
            # ---
        self._layers_updates.clear()
        # ---
        if lock:
            self._lock.release()

    def validate_engine_mode(self, mode: EngineMode) -> bool:
        return True
