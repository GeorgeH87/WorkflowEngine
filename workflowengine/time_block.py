from __future__ import annotations
import time
from typing import Callable


class TimeBlock(object):

    def __init__(
        self,
        exit_callable: Callable[[float, TimeBlock], None] = None
    ) -> None:
        self.start_time: float = None
        self.exit_callable = exit_callable
        self.overall_time = 0
        self.average_time = 0
        self.measure_count = 0
        self.minimum_time = None
        self.maximum_time = None

    def __enter__(self):
        self.measure_count += 1
        self.start_time = time.time()

    def __exit__(self, exc_type, exc_value, traceback):
        elapsed_time = time.time() - self.start_time
        self.overall_time += elapsed_time
        self.average_time = self.overall_time / self.measure_count
        if not self.minimum_time or self.minimum_time > elapsed_time:
            self.minimum_time = elapsed_time
        if not self.maximum_time or self.maximum_time < elapsed_time:
            self.maximum_time = elapsed_time
        if self.exit_callable:
            self.exit_callable(elapsed_time, self)
            
    def dict(self):
        return {
            "overall_time": self.overall_time,
            "average_time": self.average_time,
            "measure_count": self.measure_count,
            "minimum_time": self.minimum_time,
            "maximum_time": self.maximum_time
        }
