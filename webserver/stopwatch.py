import time

class Stopwatch:
    def __init__(self):
        self.last_time = None

    def start(self):
        """Start or restart the stopwatch."""
        self.last_time = time.time()

    def elapsed(self):
        """
        Return the time elapsed since the last call to this method or the start.
        Resets the reference point to the current time.
        """
        if self.last_time is None:
            raise ValueError("Stopwatch has not been started.")
        
        now = time.time()
        elapsed = now - self.last_time  # Calculate elapsed time
        self.last_time = now  # Reset last time to now
        return elapsed
        
    def resetElapsed(self):
        val = elapsed()
        start()
        return val