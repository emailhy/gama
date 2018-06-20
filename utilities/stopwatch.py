import time


class Stopwatch:
    """ A context manager that keeps track of wall clock time spent."""
    __slots__ = ['_start', '_end', 'is_running']

    def __init__(self):
        self.is_running = False
        self._start = 0
        self._end = 0

    def __enter__(self):
        self.is_running = True
        self._start = time.time()
        return self

    def __exit__(self, *args):
        self._end = time.time()
        self.is_running = False
        return False  # do not suppress any exceptions.

    @property
    def elapsed_time(self):
        if self.is_running:
            return time.time() - self._start
        else:
            return self._end - self._start


