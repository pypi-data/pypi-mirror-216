# -*- coding: UTF-8 -*-

from os import name
from typing import IO

from .constants import LOCK
from .exceptions import AlreadyLocked, LockException

__all__ = ["lock", "unlock"]

if name.upper() == "NT":
    from msvcrt import get_osfhandle
    from pywintypes import OVERLAPPED, error as PywinTypesError
    from win32con import LOCKFILE_FAIL_IMMEDIATELY, LOCKFILE_EXCLUSIVE_LOCK
    from win32file import LockFileEx, UnlockFileEx
    from winerror import ERROR_LOCK_VIOLATION, ERROR_NOT_LOCKED

    __overlapped = OVERLAPPED()


    def lock(handle: IO, flags: int):
        mode = 0
        if flags & LOCK.NB:
            mode |= LOCKFILE_FAIL_IMMEDIATELY

        if flags & LOCK.EX:
            mode |= LOCKFILE_EXCLUSIVE_LOCK

        # Save the old position, so we can go back to that position but
        # still lock from the beginning of the file
        save_position = handle.tell()
        if save_position:
            handle.seek(0)

        os_fh = get_osfhandle(handle.fileno())
        try:
            LockFileEx(os_fh, mode, 0, -0x10000, __overlapped)
        except PywinTypesError as exc_value:
            # error: (
            #   33,
            #   'LockFileEx',
            #   'The process cannot access the file because another process has locked a portion of the file.'
            # )
            if exc_value.winerror == ERROR_LOCK_VIOLATION:
                raise AlreadyLocked(
                    LockException.LOCK_FAILED,
                    exc_value.strerror,
                    handle=handle
                )
            else:
                # Q:  Are there exceptions/codes we should be dealing with here?
                raise
        finally:
            if save_position:
                handle.seek(save_position)


    def unlock(handle: IO):
        try:
            save_position = handle.tell()
            if save_position:
                handle.seek(0)

            os_fh = get_osfhandle(handle.fileno())
            try:
                UnlockFileEx(
                    os_fh, 0, -0x10000, __overlapped
                )
            except PywinTypesError as exc:
                if exc.winerror == ERROR_NOT_LOCKED:
                    # error: (158, 'UnlockFileEx', 'The segment is already unlocked.')
                    # To match the 'posix' implementation, silently ignore this error
                    pass
                else:
                    # Q:  Are there exceptions/codes we should be dealing with here?
                    raise
            finally:
                if save_position:
                    handle.seek(save_position)
        except IOError as exc:
            raise LockException(
                LockException.LOCK_FAILED,
                exc.strerror,
                handle=handle
            )

elif name.upper() == "POSIX":
    from fcntl import flock


    def lock(handle: IO, flags: int):
        locking_exceptions = IOError,
        try:
            locking_exceptions += BlockingIOError,
        except NameError:
            pass

        # Locking with NB without EX or SH enabled results in an error
        if (flags & LOCK.NB) and (not flags & (LOCK.SH | LOCK.EX)):
            raise RuntimeError(
                "When locking in NB (non-blocking) mode the SH (shared) "
                "or EX (exclusive) flag must be specified as well."
            )

        try:
            flock(handle.fileno(), flags)
        except locking_exceptions as exc_value:
            # The exception code varies on different systems, so we'll catch every IO error
            raise LockException(exc_value, handle=handle)


    def unlock(handle: IO):
        flock(handle.fileno(), LOCK.UN)

else:
    raise RuntimeError("File locking is defined only for 'NT' and 'POSIX' platforms!")
