import logging
from abc import ABC
from collections import defaultdict
from threading import Semaphore
from typing import Dict, List, Callable

from dt_duckiematrix_messages import CBorMessage
from dt_duckiematrix_protocols.commons.ProtocolAbs import ProtocolAbs


class CBORProtocol(ProtocolAbs, ABC):

    def __init__(self, engine_hostname: str, group: str, auto_commit: bool = False):
        super(CBORProtocol, self).__init__(engine_hostname, group, auto_commit)
        self._messages: Dict[str, List[CBorMessage]] = defaultdict(list)
        self._lock = Semaphore()
        self._logger = logging.getLogger(f"CBORProtocol[{group}]")

    def publish(self, key: str, message: CBorMessage):
        with self._lock:
            self._messages[key].append(message)
            # auto-commit?
            if self._auto_commit:
                self.commit(lock=False)

    def subscribe(self, key: str, msg_type: type, callback: Callable):
        self._socket.subscribe(key, msg_type, callback)

    def unsubscribe(self, key: str, callback: Callable):
        self._socket.unsubscribe(key, callback)

    def commit(self, lock: bool = True):
        if lock:
            self._lock.acquire()
        # ---
        for key, messages in self._messages.items():
            for msg in messages:
                self._socket.publish(key, msg)
            # ---
            messages.clear()
        # ---
        if lock:
            self._lock.release()
