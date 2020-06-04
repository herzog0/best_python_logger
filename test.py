import os
import time
import logging
from safe_logger import TimedRotatingFileHandlerSafe

class NullHandler(logging.Handler):
    def emit(self, record):
        pass
    def write(self, *args, **kwargs):
        pass


LOG_FILE = 'logs/debug.log'
ERR_FILE = 'logs/error.log'

FORMAT = '[%(asctime)s] [%(levelname)s] [PID: '+str(os.getpid())+'] [%(name)s]:  %(message)s'
FORMATTER = logging.Formatter(FORMAT)


logging.basicConfig(level=logging.DEBUG, stream=NullHandler())
root = logging.root
log_handler = TimedRotatingFileHandlerSafe(LOG_FILE, when='MIDNIGHT')
log_handler.setLevel(logging.DEBUG)
log_handler.setFormatter(FORMATTER)
root.addHandler(log_handler)

err_handler = TimedRotatingFileHandlerSafe(ERR_FILE, when='MIDNIGHT')
err_handler.setLevel(logging.ERROR)
err_handler.setFormatter(FORMATTER)
root.addHandler(err_handler)

lg = logging.getLogger('testme')
while True:
    lg.debug('test debug')
    lg.error('test error')
    time.sleep(0.5)
