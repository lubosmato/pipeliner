import copy
import logging
import re
from abc import ABC, abstractmethod
from typing import List, Any, Tuple
from datetime import datetime

from pipeliner.steps.step import Step

logger = logging.getLogger(__name__)


class Schedule:
    class Value(ABC):
        @abstractmethod
        def match(self, value: int) -> bool:
            pass

    class NumberValue(Value):
        def __init__(self, value: int):
            self._value = value

        def match(self, value: int) -> bool:
            return value == self._value

    class EveryNthValue(Value):
        def __init__(self, value: int):
            self._value = value

        def match(self, value: int) -> bool:
            return value % self._value == 0

    class RangeValue(Value):
        def __init__(self, range_from: int, range_to: int):
            self._from = range_from
            self._to = range_to

        def match(self, value: int) -> bool:
            return self._from <= value <= self._to

    def __init__(self, time_string: str):
        parts = re.split(r"\s+", time_string)
        are_parts_ok = all(
            re.match(r"^(\d+|\*|\*/\d+|\d+-\d+)$", part)
            for part in parts
        )
        if not are_parts_ok or len(parts) != 5:
            raise ValueError("Invalid time string format")

        self._minute = self._make_value(parts[0], (0, 59))
        self._hour = self._make_value(parts[1], (0, 23))
        self._day_of_month = self._make_value(parts[2], (1, 31))
        self._month = self._make_value(parts[3], (1, 12))
        self._day_of_week = self._make_value(parts[4], (0, 7))

    def _make_value(self, value: str, allowed_range: Tuple[int, int]) -> Value:
        if value == "*":
            return Schedule.EveryNthValue(1)
        elif re.match(r"^\d+$", value):
            parsed = int(value)
            self._check_range(parsed, allowed_range)
            return Schedule.NumberValue(parsed)
        elif re.match(r"^\*/\d+$", value):
            parsed = int(value.split("/")[1])
            self._check_range(parsed, allowed_range)
            return Schedule.EveryNthValue(parsed)
        elif re.match(r"^\d+-\d+$", value):
            range_parts = value.split("-")
            range_from = int(range_parts[0])
            range_to = int(range_parts[1])
            self._check_range(range_from, allowed_range)
            self._check_range(range_to, allowed_range)
            return Schedule.RangeValue(range_from, range_to)

        logger.error(f"Invalid schedule value")
        raise ValueError("Invalid schedule value")

    @staticmethod
    def _check_range(value: int, allowed_range: Tuple[int, int]):
        if not (allowed_range[0] <= value <= allowed_range[1]):
            raise ValueError("value is not in allowed range")

    def should_run(self, when: datetime = datetime.now()):
        if not self._minute.match(when.minute):
            return False
        if not self._hour.match(when.hour):
            return False
        if not self._day_of_month.match(when.day):
            return False
        if not self._month.match(when.month):
            return False
        if not self._day_of_week.match(when.weekday()):
            return False
        return True


class Pipeline:
    STEP_REPEAT_TRY_COUNT = 3
    _current_data: Any

    def __init__(self, name: str, schedule: str, steps: List[Step]):
        self._name = name
        self._schedule = Schedule(schedule)
        self._steps = steps
        self._current_data = None

    def run(self) -> None:
        logger.info(f"Starting pipeline \"{self.name}\"")
        try:
            self._current_data = None
            for step in self._steps:
                self._perform_step(step)
            logger.info(f"Pipeline \"{self.name}\" has finished")
        except Exception as e:
            logger.error(f"Pipeline \"{self.name}\" has failed because {e}")
            raise e

    def _perform_step(self, step: Step):
        logger.info(f"Pipeline \"{self.name}\", step {step}")

        last_exception = None
        for _ in range(self.STEP_REPEAT_TRY_COUNT):
            try:
                copied_data = copy.deepcopy(self._current_data)
                self._current_data = step.perform(copied_data)
                logger.info(f"Pipeline \"{self.name}\" has been finished")
                return
            except Exception as e:
                logger.warning(f"Pipeline \"{self.name}\": {step} has failed: {e}. Retrying.")
                last_exception = e

        if last_exception:
            logger.error(f"Pipeline \"{self.name}\": {step} has failed too many times.")
            raise last_exception

    @property
    def name(self) -> str:
        return self._name

    @property
    def schedule(self) -> Schedule:
        return self._schedule
