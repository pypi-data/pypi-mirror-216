import time

# -----------------------------------------------------------------------------


def secs_to_mins(seconds):
    """Converts seconds to minutes."""
    # return str(datetime.timedelta(seconds=seconds))
    return time.strftime("%H:%M:%S", time.gmtime(seconds))


class Timer(object):
    """Timer to simplify timing of execution."""

    def start(self):
        self.start_time = time.time()
        return self

    def stop(self):
        self.end_time = time.time()
        return self

    def elapsed(self):
        return secs_to_mins(self.end_time - self.start_time)
