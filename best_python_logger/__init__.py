import logging.handlers
import threading
import logging
import random
import fcntl
import gzip
import time
import sys
import os
import io


_lock = threading.RLock()


# Took this class from here: https://github.com/cybergrind/safe_logger
class TimedRotatingFileHandlerSafe(logging.handlers.TimedRotatingFileHandler):

    def __init__(self, filename, when='midnight', backup_count=30, **kwargs):
        super(TimedRotatingFileHandlerSafe, self).__init__(filename, when=when, backupCount=backup_count, **kwargs)

    def _open(self):
        if getattr(self, '_lockf', None) and not self._lockf.closed:
            return open(self.baseFilename, self.mode, encoding=self.encoding)
        with _lock:
            while True:
                try:
                    self._acquire_lock()
                    return open(self.baseFilename, self.mode, encoding=self.encoding)
                except (IOError, BlockingIOError):
                    self._release_lock()
                    time.sleep(random.random())
                finally:
                    self._release_lock()

    def _acquire_lock(self):
        try:
            self._lockf = open(self.baseFilename + '_rotating_lock', 'a')
        except PermissionError:
            name = './{}_rotating_lock'.format(os.path.basename(self.baseFilename))
            self._lockf = open(name, 'a')
        fcntl.flock(self._lockf, fcntl.LOCK_EX | fcntl.LOCK_NB)

    def _release_lock(self):
        if not self._lockf.closed:
            fcntl.lockf(self._lockf, fcntl.LOCK_UN)
            self._lockf.close()

    @staticmethod
    def is_same_file(file1, file2):
        """check is files are same by comparing inodes"""
        return os.fstat(file1.fileno()).st_ino == os.fstat(file2.fileno()).st_ino

    def doRollover(self):
        """
        do a rollover; in this case, a date/time stamp is appended to the filename
        when the rollover happens.  However, you want the file to be named for the
        start of the interval, not the current time.  If there is a backup count,
        then we have to get a list of matching filenames, sort them and remove
        the one with the oldest suffix.
        """
        with _lock:
            return self._innerDoRollover()

    def _innerDoRollover(self):
        try:
            self._acquire_lock()
        except (IOError, BlockingIOError):
            # cant acquire lock, return
            self._release_lock()
            return

        # get the time that this sequence started at and make it a time_tuple
        t = self.rolloverAt - self.interval
        if self.utc:
            time_tuple = time.gmtime(t)
        else:
            time_tuple = time.localtime(t)
        dfn = self.baseFilename + "." + time.strftime(self.suffix, time_tuple) + ".txt" + ".gz"

        # check if file is same
        try:
            if self.stream:
                with open(self.baseFilename, 'r') as _tmp_f:
                    is_same = self.is_same_file(self.stream, _tmp_f)

                if self.stream:
                    self.stream.close()
                if is_same and not os.path.exists(dfn):
                    with open(self.baseFilename, "rb+") as sf:
                        data = sf.read()
                        compressed = gzip.compress(data, 9)
                        with open(dfn, "wb") as df:
                            df.write(compressed)
                    os.remove(self.baseFilename)
        except ValueError:
            # ValueError: I/O operation on closed file
            is_same = False

        if self.backupCount > 0:
            for s in self.getFilesToDelete():
                os.remove(s)
        self.mode = 'a'
        self.stream = self._open()
        current_time = int(time.time())
        new_rollover_at = self.computeRollover(current_time)
        while new_rollover_at <= current_time:
            new_rollover_at = new_rollover_at + self.interval

        # If DST changes and midnight or weekly rollover, adjust for this.
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            dst_now = time.localtime(current_time)[-1]
            dst_at_rollover = time.localtime(new_rollover_at)[-1]
            if dst_now != dst_at_rollover:
                if not dst_now:  # DST kicks in before next rollover, so we need to deduct an hour
                    new_rollover_at = new_rollover_at - 3600
                else:           # DST bows out before next rollover, so we need to add an hour
                    new_rollover_at = new_rollover_at + 3600
        self.rolloverAt = new_rollover_at
        self._release_lock()


def color_cheat_sheet():
    # This doesn't work very good in IDEs python consoles.
    terse = "-t" in sys.argv[1:] or "--terse" in sys.argv[1:]
    write = sys.stdout.write
    for i in range(2 if terse else 10):
        for j in range(30, 38):
            for k in range(40, 48):
                if terse:
                    write("\33[%d;%d;%dm%d;%d;%d\33[m " % (i, j, k, i, j, k))
                else:
                    write("%d;%d;%d: \33[%d;%d;%dm Hello, World! \33[m \n" %
                          (i, j, k, i, j, k,))
            write("\n")


class __CustomFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors"""

    grey = "\x1b[0;37m"
    green = "\x1b[1;32m"
    yellow = "\x1b[1;33m"
    red = "\x1b[1;31m"
    purple = "\x1b[1;35m"
    blue = "\x1b[1;34m"
    light_blue = "\x1b[1;36m"
    reset = "\x1b[0m"
    blink_red = "\x1b[5m\x1b[1;31m"
    format_prefix = f"{purple}%(asctime)s{reset} " \
                    f"{blue}%(name)s{reset} " \
                    f"{light_blue}(%(filename)s:%(lineno)d){reset} "

    format_suffix = "%(levelname)s - %(message)s"

    FORMATS = {
        logging.DEBUG: format_prefix + green + format_suffix + reset,
        logging.INFO: format_prefix + grey + format_suffix + reset,
        logging.WARNING: format_prefix + yellow + format_suffix + reset,
        logging.ERROR: format_prefix + red + format_suffix + reset,
        logging.CRITICAL: format_prefix + blink_red + format_suffix + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


# Just import this function into your programs
# "from logger import get_logger"
# "logger = get_logger(__name__)"
# Use the variable __name__ so the logger will print the file's name also
class __NullHandler(io.StringIO):
    def emit(self, record):
        pass

    def write(self, *args, **kwargs):
        pass


def get_logger(name, filename="logs/my_program.log", when="midnight", interval=1, backup_count=5, visible_stream=False):

    if not os.path.exists("logs/"):
        os.mkdir("logs/")

    logging.basicConfig(level=logging.DEBUG, stream=__NullHandler())
    root = logging.root

    fh = TimedRotatingFileHandlerSafe(filename=filename, when=when, interval=interval,
                                      backup_count=backup_count)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(__CustomFormatter())
    root.addHandler(fh)

    if visible_stream:
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(__CustomFormatter())
        root.addHandler(ch)

    return logging.getLogger(name)
