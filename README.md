# Best Python logger

This is the best python logger. 
It doesn't require additional packages. 
It is so great that deserved its own repo.

Stolen and modified from [here](https://stackoverflow.com/a/56944256/12603421) and [here](https://github.com/cybergrind/safe_logger)
## Using the logger

## Simplest usage
```python
from best_python_logger import get_logger
logger = get_logger(__name__)
# Use the variable __name__ so the logger will print the file's name also

logger.debug("<some important rocket science phrase>")
logger.info("Awesome!")
logger.error("Ok, we are in trouble.")
logger.critical("Damn blinks that doesn't work on most IDEs built-in terminals..")
```




## README of one of the sources 

(I though it would be useful for some people to read the comments of the owner of safe_logger package)
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

