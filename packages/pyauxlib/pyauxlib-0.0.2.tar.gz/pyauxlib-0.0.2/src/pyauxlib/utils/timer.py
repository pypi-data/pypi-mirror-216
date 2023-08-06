import csv
import logging
import time
import warnings
from pathlib import Path


class Timer:
    """Timer class to measure execution times.

    The timer can be managed manually, calling the start, stop,... methods.
    It can also be used as a context manager:
    ```python
    with Timer(file) as t: # This will automaticall start the timer
        # code here
        t.add_timestamp("#1")
        # more code
    # The timer will automatically be stopped when exiting the context manager
    ```

    Parameters
    ----------
    filename : str | Path | None
        The name or path of the file to save the timestamps.
    time_func : callable, optional
        The time function to use. It can be time.time, time.perf_counter or
        time.process_time. By default time.time.
    logger : logging.Logger, optional
        The logger to use for logging warnings. By default None.

    Attributes
    ----------
    filename : str | Path | None
        The name of the file to save the timestamps. By default None.
    start_time : float or None
        The start time of the timer.
    stop_time : float or None
        The stop time of the timer.
    timestamps : list of float
        The list of timestamps added during the timer execution.
    texts : list of str
        The list of texts associated with each timestamp.
    """

    def __init__(
        self,
        filename: str | Path | None = None,
        time_func=time.time,
        logger: logging.Logger | None = None,
    ):
        self.filename = filename
        self.time_func = time_func
        self.logger = warnings.warn if logger is None else logger.warning
        self.where_output = None if logger is None else logger.info
        self.reset()

    def __enter__(self):
        """Start a new timer as a context manager"""
        self.start()
        return self

    def __exit__(self, *exc_info):
        """Stop the context manager timer"""
        self.stop()

    def start(self):
        """Starts the timer."""
        if self.stop_time is not None:
            self.logger("Timer has not been resetted.")
            return
        self.start_time = self.time_func()

    def stop(self) -> float:
        """Stops the timer and returns the ellapsed time. It also saves the timestamps
        to a file, when provided."""
        if self.start_time is None:
            self.logger("Timer has not been started.")
            return 0

        self.stop_time = self.time_func()
        self.texts.append("stop")
        self.save()

        ellapsed_time = self.stop_time - self.start_time

        if self.where_output is not None:
            self.where_output(f"Ellapsed time: {ellapsed_time} s")

        return ellapsed_time

    def add_timestamp(self, text=""):
        """Adds a timestamp with an associated text.

        Parameters
        ----------
        text : str, optional
            The text associated with the timestamp. By default "".
        """
        if self.start_time is None:
            self.logger("Timer has not been started.")
            return
        if self.stop_time is not None:
            self.logger("Timer is stopped.")
            return

        self.timestamps.append(self.time_func())
        self.texts.append(text)

    def save(self):
        """Saves the timestamps and their associated texts to a file."""
        if self.start_time is None:
            self.logger("Timer has not been started.")
            return
        if self.stop_time is None:
            self.logger("Timer has not been stopped yet.")
            return
        if self.filename is None:
            return

        with Path.open(self.filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            header = ["Comment", "Timestamp", "Time", "Elapsed Time", "Total Time"]
            writer.writerow(header)

            formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.start_time))
            row = [self.texts[0], self.start_time, formatted_time, 0, 0]
            writer.writerow(row)
            prev_time = self.start_time
            for i, timestamp in enumerate(self.timestamps):
                elapsed_time = timestamp - prev_time
                total_time = timestamp - self.start_time
                formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
                row = [
                    self.texts[i + 1],
                    timestamp,
                    formatted_time,
                    elapsed_time,
                    total_time,
                ]
                writer.writerow(row)
                prev_time = timestamp
            elapsed_time = self.stop_time - prev_time
            total_time = self.stop_time - self.start_time
            formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.stop_time))
            row = [
                self.texts[-1],
                self.stop_time,
                formatted_time,
                elapsed_time,
                total_time,
            ]
            writer.writerow(row)

    def reset(self):
        """Resets the timer."""
        self.start_time = None
        self.stop_time = None
        self.timestamps = []
        self.texts = ["start"]
