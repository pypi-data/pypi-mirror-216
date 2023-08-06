# -*- coding: UTF-8 -*-

from abc import ABC, abstractmethod
from os import fsync
from os.path import realpath
from threading import RLock
from typing import Union, IO, TextIO, BinaryIO

from .constants import LOCK, RLOCKS, NAME
from .core import lock, unlock
from .exceptions import LockFlagsError

__all__ = [
    "BaseFileLocker",
    "FileLocker",
    "BaseFileHandler",
    "FileHandler"
]


class BaseFileLocker(ABC):
    """Base abstract handler."""

    def __init__(self, *args, **kwargs):
        self._args, self._kwargs = args, kwargs

    def __enter__(self) -> Union[IO, TextIO, BinaryIO]:
        if not hasattr(self, "_handle"):
            self._handle: Union[IO, TextIO, BinaryIO] = self.acquire(*self._args, **self._kwargs)
        return self._handle

    def __exit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self, "_handle"):
            self.release(self._handle)
            del self._handle

    def __delete__(self, instance):
        instance.release()

    @abstractmethod
    def acquire(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def release(self, *args, **kwargs):
        raise NotImplementedError


class FileLocker(BaseFileLocker):
    """File locker."""

    _flags: dict = {
        "w": LOCK.EX,
        "a": LOCK.EX,
        "x": LOCK.EX,
        "r": LOCK.SH,
    }

    def acquire(self, handle: Union[IO, TextIO, BinaryIO], flags: LOCK = None) -> Union[IO, TextIO, BinaryIO]:
        """
        Acquire a lock on the given `handle`.
        If `flags` are not provided it will try to guess
        them by reading the handle's operating mode.

        :param handle: The file handle.
        :param flags: The flags to be used to lock the handle.
        :return: The newly locked handle.
        """
        mode = self._get_mode(handle)

        if flags is None:
            flags = self._flags.get(mode)

        elif (mode == "w") and (flags in (LOCK.SH | LOCK.NB)):
            raise LockFlagsError(f"Wrong flags used on this operating mode of the handle (`{mode}`)!")

        lock(handle, flags)
        return handle

    def release(self, handle: Union[IO, TextIO, BinaryIO]):
        """Unlock the file handle."""
        unlock(handle)

    @staticmethod
    def _get_mode(handle: Union[IO, TextIO, BinaryIO]) -> str:
        """Return the handle's operating mode."""
        mode = handle.mode
        return mode.strip("tb+")


class BaseFileHandler(ABC):
    """Base abstract handler."""

    @staticmethod
    def _dispatch_rlock(name: str = NAME) -> RLock:
        if name not in RLOCKS:
            instance: RLock = RLock()
            RLOCKS.update({name: instance})
        return RLOCKS.get(name)

    def __init__(self, file: str, *args, **kwargs):
        self._file, self._args, self._kwargs = realpath(file), args, kwargs
        self._thread_lock: RLock = self._dispatch_rlock(self._file)

    def __enter__(self) -> Union[IO, TextIO, BinaryIO]:
        self._thread_lock.acquire()
        try:
            if not hasattr(self, "_handle"):
                self._handle = self._acquire(self._file, *self._args, **self._kwargs)
        except FileNotFoundError:
            self._thread_lock.release()
            raise
        else:
            return self._handle

    def __exit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self, "_handle"):
            self._release(self._handle)
            del self._handle
        self._thread_lock.release()

    def __delete__(self, instance):
        instance.release()

    @abstractmethod
    def _acquire(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def _release(self, *args, **kwargs):
        raise NotImplementedError

    def close(self):
        with self._thread_lock:
            if hasattr(self, "_handle"):
                self._release(self._handle)
                del self._handle


class FileHandler(BaseFileHandler):
    """Simple file handler."""

    _file_lock = FileLocker()

    def __init__(self, file: str, *args, **kwargs):
        super(FileHandler, self).__init__(file, *args, **kwargs)

        self._thread_lock.acquire()
        try:
            if not hasattr(self, "_handle"):
                self._handle: Union[IO, TextIO, BinaryIO] = self._acquire(self._file, *args, **kwargs)
        except FileNotFoundError:
            raise
        finally:
            self._thread_lock.release()

    def _acquire(self, file: str, *args, **kwargs) -> Union[IO, TextIO, BinaryIO]:
        """Returns a new locked file handle."""
        self._thread_lock.acquire()
        try:
            handle: Union[IO, TextIO, BinaryIO] = open(file, *args, **kwargs)
        except FileNotFoundError:
            raise
        else:
            return self._file_lock.acquire(handle)
        finally:
            self._thread_lock.release()

    def _release(self, handle: Union[IO, TextIO, BinaryIO]):
        """Close the file handle and release the resources."""
        with self._thread_lock:
            handle.flush()
            if "r" not in handle.mode:
                fsync(handle.fileno())
            self._file_lock.release(handle)
            handle.close()
