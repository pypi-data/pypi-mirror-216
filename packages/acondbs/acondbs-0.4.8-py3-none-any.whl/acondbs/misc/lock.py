import os
import time
from pathlib import Path
from typing import Optional, Union


class lock:
    def __init__(self, path: Union[Path, str], timeout: Optional[float] = None):
        self.path = Path(path)
        self.timeout = timeout
        self.locked = False

    def __enter__(self) -> 'lock':
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.release()

    def acquire(self) -> None:
        start_time = time.time()
        while True:
            if try_make_file(self.path):
                break
            if self.timeout is not None:
                if time.time() - start_time > self.timeout:
                    raise TimeOutAcquiringLock
            time.sleep(0.001)
        self.locked = True

    def release(self) -> None:
        if not self.locked:
            return

        try:
            self.path.unlink()
        except FileNotFoundError:
            pass
        self.locked = False


class TimeOutAcquiringLock(Exception):
    pass


def try_make_file(path: Union[str, Path]) -> bool:
    """try to create a file atomically

    http://stackoverflow.com/questions/33223564/atomically-creating-a-file-if-it-doesnt-exist-in-python
    """
    try:
        os.open(path, os.O_CREAT | os.O_EXCL)
        return True
    except FileExistsError:
        return False
