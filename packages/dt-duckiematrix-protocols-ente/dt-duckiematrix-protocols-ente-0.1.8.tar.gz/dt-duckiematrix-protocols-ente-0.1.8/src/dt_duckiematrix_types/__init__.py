from enum import IntEnum


class NetworkRole(IntEnum):
    RENDERER = 1
    CLIENT = 2


class EngineMode(IntEnum):
    REALTIME = 0
    GYM = 1
