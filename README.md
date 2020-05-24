# Best Python logger

This is the best python logger. 
It doesn't require additional packages. 
It is so great that deserved its own repo.

Stolen and modified from [here](https://stackoverflow.com/a/56944256/12603421)

## Using the logger

```python
from logger import get_logger
logger = get_logger(__name__)
# Use the variable __name__ so the logger will print the file's name also

logger.debug("<some important rocket science phrase>")
logger.info("Awesome!")
logger.error("Ok, we are in trouble.")
logger.critical("Damn blinks that doesn't work on most IDEs built-in terminals..")
```
