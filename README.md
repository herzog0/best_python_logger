# Best Python logger

(For the record, I discovered [loguru](https://github.com/Delgan/loguru) and if it fulfill my needs I'm gonna abandon this project)


This is the best python logger. 
It doesn't require additional packages. 
It is so great that deserved its own repo.

Stolen and modified from [here](https://stackoverflow.com/a/56944256/12603421) and [here](https://github.com/cybergrind/safe_logger)


# Usage

### Simplest usage
```python
from best_python_logger import get_logger
logger = get_logger(__name__)
# Use the variable __name__ so the logger will print the file's name also

logger.debug("<some important rocket science phrase>")
logger.info("Awesome!")
logger.error("Ok, we are in trouble.")
logger.critical("Damn blinks that doesn't work on most IDEs built-in terminals..")
```

### Master usage
```python
import time
from best_python_logger import get_logger
import logging

test_logger = get_logger(name=__name__,
                         filename="logs/test/dirs/test.log",
                         when="S",
                         interval=3,
                         backup_count=3,
                         visible_stream=True,
                         compress=True,
                         auto_colorized=True,
                         custom_format=None,
                         only_visible_stream_auto_colorized=True,
                         level=logging.INFO)

count = 0
while True:
    count += 1
    time.sleep(0.001)
    test_logger.debug("hi, " + str(count))
```



## README of one of the sources 

(I though it would be useful for some people to read the comments of the owner of safe_logger package, from which I got the concurrency fix part)
```
## Description

This handler is designed to provide correct log files rotation when multiple processes writing to file.

Heavilly tested on production systems with up to 50 writers.

**Caveat**: this logger has been extracted from other system, so can have issues cause by copy-pasting

## Pitfalls

* Naive aproach fails because concurrent processes do independent rollovers and finally you will have zero-lenght log file: so we need locking
* Naive locking fails when you have some processes that not write often and them can rotate you file in case you archive old, or etc.: so we need check file that want to move by compare inodes
* Naive approach to start handler have issues, when you open file that in rollover - you can write data to rotated file: so we need locking on open file
```

