import time

class Stopwatch:
    def __init__(self):
        self.last_time = 0.0

    def start(self):
        """Start or restart the stopwatch."""
        self.last_time = time.time()

    def elapsed(self):
        """
        Return the time elapsed since the last call to this method or the start.
        Resets the reference point to the current time.
        """
        now = time.time()
        elapsed = now - self.last_time  # Calculate elapsed time
        self.last_time = now  # Reset last time to now
        return elapsed
        
    def resetElapsed(self):
        val = self.elapsed()
        self.start()
        return val