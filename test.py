import time
from best_python_logger import get_logger
test_logger = get_logger(name=__name__,
                         filename="logs/test.log",
                         when="S",
                         interval=3,
                         backup_count=3,
                         visible_stream=True)

count = 0
while True:
    count += 1
    time.sleep(1)
    test_logger.debug("hi, " + str(count))
