import logging
import time
from threading import Thread, Semaphore
from typing import Callable, Dict, Set, Optional, Tuple

import zmq
from cbor2 import loads

from dt_duckiematrix_messages import CBorMessage
from dt_duckiematrix_messages.StringMessage import StringMessage

logging.basicConfig()


class DuckieMatrixEngineSocketAbs(Thread):

    def __init__(self, name: str):
        super(DuckieMatrixEngineSocketAbs, self).__init__(daemon=True)
        self._context: zmq.Context = zmq.Context()
        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.INFO)

    @staticmethod
    def _get_uri(protocol: str, hostname: str, port: int):
        if protocol == "icp":
            return f"{protocol}://{hostname}"
        else:
            return f"{protocol}://{hostname}:{port}"


class DuckieMatrixEngineDataSocket(DuckieMatrixEngineSocketAbs):

    def __init__(self, group: str,
                 in_uri: Optional[str] = None, out_uri: Optional[str] = None):
        super(DuckieMatrixEngineDataSocket, self).__init__(f"DataSocket[{group}]")
        self._in_uri: Optional[str] = in_uri
        self._out_uri: Optional[str] = out_uri
        self._in_socket: Optional[zmq.Socket] = None
        self._out_socket: Optional[zmq.Socket] = None
        # socket IN
        if self._in_uri is not None:
            self._logger.info(f"Establishing link to DATA IN connector for group '{group}' "
                              f"at {in_uri}...")
            try:
                socket: zmq.Socket = self._context.socket(zmq.SUB)
                socket.connect(in_uri)
                self._in_socket = socket
                self._logger.info(f"Link to DATA IN connector for group '{group}' established "
                                  f"at {in_uri}.")
            except BaseException as e:
                self._logger.error(str(e))
        # socket OUT
        if self._out_uri is not None:
            self._logger.info("Establishing link to DATA OUT connector "
                              f"for group '{group}' at {out_uri}...")
            try:
                socket: zmq.Socket = self._context.socket(zmq.PUB)
                socket.connect(out_uri)
                self._out_socket = socket
                self._logger.info(f"Link to DATA OUT connector for group '{group}' established "
                                  f"at {out_uri}.")
            except BaseException as e:
                self._logger.error(str(e))
        # ---
        self.decoders: Dict[str, type] = {}
        self.callbacks: Dict[str, Set[Callable]] = {}
        self.is_shutdown = False

    @property
    def connected(self) -> bool:
        needs_in_socket = self._in_uri is not None
        needs_out_socket = self._out_uri is not None
        has_in_socket = self._in_socket is not None
        has_out_socket = self._out_socket is not None
        return (not needs_in_socket or has_in_socket) and (not needs_out_socket or has_out_socket)

    def wait_until_connected(self):
        while not self.connected:
            time.sleep(0.1)

    def release(self):
        # close sockets
        sockets = {
            self._in_uri: self._in_socket,
            self._out_uri: self._out_socket,
        }
        for uri, socket in sockets.items():
            if uri is not None and socket is not None:
                try:
                    socket.disconnect(uri)
                except Exception as e:
                    self._logger.error(str(e))
                try:
                    socket.close()
                except Exception as e:
                    self._logger.error(str(e))

    def shutdown(self, block: bool = True):
        self.is_shutdown = True
        self.release()
        if block:
            self.join()

    def subscribe(self, key: str, msg_type: type, callback: Callable):
        if self._in_socket is None:
            self._logger.error("You are subscribing to a data connector without IN socket.")
            return
        # ---
        if self.connected:
            # register key -> msg_type mapping
            self.decoders[key] = msg_type
            # register key -> callback mapping
            if key not in self.callbacks:
                self.callbacks[key] = set()
            self.callbacks[key].add(callback)
            # subscribe to key
            self._in_socket.setsockopt_string(zmq.SUBSCRIBE, key)
        else:
            raise Exception("Socket not connected. Cannot subscribe to a key.")

    def unsubscribe(self, key: str, callback: Callable):
        if self._in_socket is None:
            self._logger.error("You are unsubscribing from a data connector without IN socket.")
            return
        # ---
        if self.connected:
            # remove key -> msg_type mapping
            if key in self.decoders:
                del self.decoders[key]
            # remove key -> callback mapping
            if key in self.callbacks:
                self.callbacks[key].remove(callback)
                if len(self.callbacks[key]) <= 0:
                    del self.callbacks[key]
            # unsubscribe
            self._in_socket.setsockopt_string(zmq.UNSUBSCRIBE, key)
        else:
            raise Exception("Socket not connected. Cannot unsubscribe a key.")

    def publish(self, key: str, message: CBorMessage):
        if self._out_socket is None:
            self._logger.error("You are publish to a data connector without OUT socket.")
            return
            # ---
        key_raw = key.encode("ascii")
        message_raw = message.to_bytes()
        self._out_socket.send_multipart([key_raw, message_raw])

        # TODO: remove
        # print(f"PUBLISH: [{key}]: {message}")

    def run(self) -> None:
        if self._in_socket is None:
            return
        # ---
        while not self.is_shutdown:
            key, data = self._in_socket.recv_multipart()
            key = key.decode("ascii").strip()
            # noinspection PyUnresolvedReferences
            if key in self.callbacks:
                message = loads(data)
                Decoder = self.decoders[key]
                message = Decoder(**message)
                for cback in self.callbacks[key]:
                    cback(message)


class DuckieMatrixEngineControlSocket(DuckieMatrixEngineSocketAbs):

    def __init__(self, hostname: str, protocol: str = "tcp", port: int = 7501):
        super(DuckieMatrixEngineControlSocket, self).__init__("ControlSocket")
        self._hostname = hostname
        self._uri: str = self._get_uri(protocol, hostname, port)
        # socket OUT
        self._logger.info(f"Establishing link to CONTROL connector at {self._uri}...")
        try:
            socket: zmq.Socket = self._context.socket(zmq.REQ)
            socket.connect(self._uri)
            self._socket = socket
        except BaseException as e:
            self._logger.error(str(e))
        # ---
        self._lock = Semaphore()
        self.is_shutdown = False

    @property
    def connected(self) -> bool:
        return self._socket is not None

    def release(self):
        # close socket
        if self._socket is not None:
            try:
                self._socket.disconnect(self._uri)
            except Exception as e:
                self._logger.error(str(e))
            try:
                self._socket.close()
            except Exception as e:
                self._logger.error(str(e))

    def shutdown(self, block: bool = True):
        self.is_shutdown = True
        self.release()
        if block:
            self.join()

    def request(self, key: str, message: CBorMessage) -> Tuple[Optional[str], bytes]:
        with self._lock:
            key_raw = key.encode("ascii")
            message_raw = message.to_bytes()
            # send request
            self._socket.send_multipart([key_raw, message_raw])
            # wait for reply
            key_raw, message_raw = self._socket.recv_multipart()
            key = key_raw.decode("ascii")
            # common replies
            if key == "request/error":
                message = StringMessage.from_bytes(message_raw)
                self._logger.error(f"The engine responded with the message: {message.value}")
                return None, b""
            # ---
            return key, message_raw

