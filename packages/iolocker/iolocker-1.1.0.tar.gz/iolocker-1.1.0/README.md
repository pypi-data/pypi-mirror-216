# iolocker

Simple file locker.

---

#### Installation:

```commandline
python -m pip install [--upgrade] iolocker
```

---


#### Usage:

###### FileLocker:

```python
# -*- coding: UTF-8 -*-

from iolocker import FileLocker, LOCK

if __name__ == '__main__':

    file_handle = open("test_file.txt", "a", encoding="UTF-8")
    lock = FileLocker()

    fh = lock.acquire(file_handle, flags=LOCK.EX)
    fh.write("Testing file lockers...\n")
    lock.release(handle=fh)
```

or as context-manager:

```python
# -*- coding: UTF-8 -*-

from iolocker import FileLocker, LOCK

if __name__ == '__main__':

    with open("test_file.txt", "a", encoding="UTF-8") as fh:
        with FileLocker(fh, flags=LOCK.EX) as locked:
            locked.write("Testing file lockers...\n")
```


###### FileHandler:

```python
# -*- coding: UTF-8 -*-

from iolocker import FileHandler


if __name__ == '__main__':

    file_path: str = r"test_file.txt"

    with FileHandler(file_path, "a", encoding="UTF-8") as fh:
        fh.write("Testing file handlers...\n")
```

---