import abc


class MonitoredObjectSessionContext:

    def __init__(self, mobj: 'MonitoredObject', override_auto_commit: bool):
        self._mobj = mobj
        self._auto_commit = mobj.auto_commit
        self._override_auto_commit = override_auto_commit

    def __enter__(self):
        self._mobj.auto_commit = self._override_auto_commit

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._mobj.auto_commit = self._auto_commit
        if self._mobj.auto_commit:
            self._mobj.commit()


class MonitoredObjectQuietContext:

    def __init__(self, mobj: 'MonitoredObject'):
        self._mobj = mobj
        self._auto_commit = mobj.auto_commit

    def __enter__(self):
        self._mobj.auto_commit = False

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._mobj.auto_commit = self._auto_commit


class MonitoredObject(abc.ABC):

    def __init__(self, auto_commit: bool = False):
        self._auto_commit = auto_commit

    @property
    def auto_commit(self) -> bool:
        return self._auto_commit

    @auto_commit.setter
    def auto_commit(self, value: bool):
        self._auto_commit = value

    def commit(self):
        self._commit()

    def session(self):
        return MonitoredObjectSessionContext(self, self._auto_commit)

    def atomic(self):
        return MonitoredObjectSessionContext(self, False)

    def quiet(self):
        return MonitoredObjectQuietContext(self)

    @abc.abstractmethod
    def _commit(self):
        pass
