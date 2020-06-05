import time
from best_python_logger import get_logger
test_logger = get_logger(name=__name__,
                         filename="logs/test/dirs/test.log",
                         when="S",
                         interval=3,
                         backup_count=3,
                         visible_stream=True,
                         compress=True,
                         auto_colorized=True,
                         custom_format=None,
                         only_visible_stream_auto_colorized=True)


count = 0
while True:
    count += 1
    time.sleep(0.01)
    test_logger.debug("hi, " + str(count))
