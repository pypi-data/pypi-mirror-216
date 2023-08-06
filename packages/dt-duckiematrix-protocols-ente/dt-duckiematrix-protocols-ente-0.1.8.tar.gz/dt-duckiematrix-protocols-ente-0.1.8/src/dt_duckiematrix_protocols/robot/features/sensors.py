import traceback
from abc import ABC
from threading import Semaphore, Thread
from typing import Optional, TypeVar, Generic, Callable, Set

from dt_duckiematrix_messages.CameraFrame import CameraFrame
from dt_duckiematrix_messages.TimeOfFlightRange import TimeOfFlightRange
from dt_duckiematrix_messages.WheelEncoderTicks import WheelEncoderTicks
from dt_duckiematrix_protocols.robot.RobotProtocols import RobotProtocolAbs
from dt_duckiematrix_protocols.utils.MonitoredCondition import MonitoredCondition


T = TypeVar('T')


class SensorAbs(Generic[T], ABC):

    def __init__(self, protocol: RobotProtocolAbs, key: str, msg_type: T):
        self._protocol = protocol
        self._key = key
        self._msg_type = msg_type
        self._enabled: bool = True
        self._shutdown: bool = False
        self._reading: T = None
        self._reading_used: bool = False
        self._lock = Semaphore()
        self._event = MonitoredCondition()
        self._callbacks: Set[Callable[[T], None]] = set()
        self._mailman: Thread = Thread(target=self._mailman_job, daemon=True)
        self._mailman.start()

    @property
    def latest(self) -> Optional[T]:
        return self._reading

    def _on_new_reading(self, msg: T):
        if not self._enabled:
            return
        with self._lock:
            self._reading = msg
            self._reading_used = True
        with self._event:
            self._event.notify_all()

    def _grab_current(self) -> Optional[T]:
        with self._lock:
            self._reading_used = True
            return self._reading

    def _mailman_job(self):
        self._protocol.wait_until_connected()
        self._protocol.subscribe(self._key, self._msg_type, self._on_new_reading)
        while not self._shutdown:
            # wait for a new message to come in
            with self._event:
                new_msg: bool = self._event.wait(0.1)
                if not new_msg:
                    continue
            # read message
            msg: T = self._reading
            # send it to the callback
            for callback in self._callbacks:
                try:
                    callback(msg)
                except Exception:
                    traceback.print_last()

    def capture(self, block: bool = False, timeout: Optional[float] = None) -> Optional[T]:
        if not block:
            return self._grab_current()
        else:
            with self._event:
                timed_out = not self._event.wait(timeout)
                if timed_out:
                    return None
                return self._grab_current()

    def start(self):
        if self._shutdown:
            raise RuntimeError("You cannot 'start' a closed sensor.")
        # ---
        self._enabled = True

    def stop(self):
        self._enabled = False

    def attach(self, callback: Callable[[T], None]):
        if self._shutdown:
            raise RuntimeError("You cannot 'attach' to a closed sensor.")
        # ---
        with self._lock:
            self._callbacks.add(callback)

    def detach(self, callback: Callable[[T], None]):
        with self._lock:
            if callback in self._callbacks:
                self._callbacks.remove(callback)

    def release(self):
        self._protocol.unsubscribe(self._key, self._on_new_reading)
        self._shutdown = True


class Camera(SensorAbs[CameraFrame]):

    def __init__(self, protocol: RobotProtocolAbs, key: str):
        super(Camera, self).__init__(protocol, key, CameraFrame)


class WheelEncoder(SensorAbs[WheelEncoderTicks]):

    def __init__(self, protocol: RobotProtocolAbs, key: str):
        super(WheelEncoder, self).__init__(protocol, key, WheelEncoderTicks)


class TimeOfFlight(SensorAbs[TimeOfFlightRange]):

    def __init__(self, protocol: RobotProtocolAbs, key: str):
        super(TimeOfFlight, self).__init__(protocol, key, TimeOfFlightRange)


__all__ = [
    Camera,
    WheelEncoder,
    TimeOfFlight
]
