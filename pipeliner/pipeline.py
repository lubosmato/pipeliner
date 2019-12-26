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
        def parse(self, token: str, allowed_range: Tuple[int, int]) -> bool:
            pass

        @abstractmethod
        def match(self, value: int) -> bool:
            pass

        @staticmethod
        def _check_range(value: int, allowed_range: Tuple[int, int]):
            if not (allowed_range[0] <= value <= allowed_range[1]):
                raise ValueError("value is not in allowed range")

    class NumberValue(Value):
        def __init__(self):
            self._value = None

        def parse(self, token: str, allowed_range: Tuple[int, int]) -> bool:
            if re.match(r"^\d+$", token):
                parsed = int(token)
                self._check_range(parsed, allowed_range)
                self._value = parsed
                return True
            return False

        def match(self, value: int) -> bool:
            return value == self._value

    class EveryNthValue(Value):
        def __init__(self):
            self._value = None

        def parse(self, token: str, allowed_range: Tuple[int, int]) -> bool:
            if re.match(r"^\*/\d+$", token):
                parsed = int(token.split("/")[1])
                self._check_range(parsed, allowed_range)
                self._value = parsed
                return True
            return False

        def match(self, value: int) -> bool:
            return value % self._value == 0

    class EveryTimeValue(EveryNthValue):
        def parse(self, token: str, allowed_range: Tuple[int, int]) -> bool:
            if token == "*":
                self._value = 1
                return True
            return False

    class RangeValue(Value):
        def __init__(self):
            self._from = None
            self._to = None

        def parse(self, token: str, allowed_range: Tuple[int, int]) -> bool:
            if re.match(r"^\d+-\d+$", token):
                range_parts = token.split("-")
                range_from = int(range_parts[0])
                range_to = int(range_parts[1])
                self._check_range(range_from, allowed_range)
                self._check_range(range_to, allowed_range)
                self._from = range_from
                self._to = range_to
                return True
            return False

        def match(self, value: int) -> bool:
            return self._from <= value <= self._to

    class MultipleValue(Value):
        def __init__(self):
            self._values = []

        def parse(self, token: str, allowed_range: Tuple[int, int]) -> bool:
            if re.match(r"^(\d+,)*\d+$", token):
                value_parts = token.split(",")
                values = [int(value) for value in value_parts]
                for value in values:
                    self._check_range(value, allowed_range)
                self._values = values
                return True
            return False

        def match(self, value: int) -> bool:
            return value in self._values

    _AVAILABLE_VALUE_TYPES = [NumberValue, EveryNthValue, EveryTimeValue, RangeValue, MultipleValue]

    def __init__(self, time_string: str):
        parts = re.split(r"\s+", time_string)
        if len(parts) != 5:
            raise ValueError("Invalid time string format")

        self._minute = self._make_value(parts[0], (0, 59))
        self._hour = self._make_value(parts[1], (0, 23))
        self._day_of_month = self._make_value(parts[2], (1, 31))
        self._month = self._make_value(parts[3], (1, 12))
        self._day_of_week = self._make_value(parts[4], (0, 7))

    def _make_value(self, value: str, allowed_range: Tuple[int, int]) -> Value:
        for ValueType in self._AVAILABLE_VALUE_TYPES:
            made_value = ValueType()
            if made_value.parse(value, allowed_range):
                return made_value

        logger.error(f"Invalid schedule value")
        raise ValueError("Invalid schedule value")

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
                logger.info(f"Step {step} in \"{self.name}\" has been finished")
                return
            except Exception as e:
                logger.warning(f"Step {step} in \"{self.name}\" has failed: {e}. Retrying.")
                last_exception = e

        if last_exception:
            logger.error(f"Step {step} in \"{self.name}\" has failed too many times.")
            raise last_exception

    @property
    def name(self) -> str:
        return self._name

    @property
    def schedule(self) -> Schedule:
        return self._schedule
