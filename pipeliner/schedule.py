import logging
import re
from abc import ABC, abstractmethod
from typing import Tuple, List, Type

from datetime import datetime

logger = logging.getLogger(__name__)


class Value(ABC):
    @abstractmethod
    def parse(self, token: str, allowed_range: Tuple[int, int]) -> bool:
        pass

    @abstractmethod
    def match(self, value: int) -> bool:
        pass

    @staticmethod
    def _check_range(value: int, allowed_range: Tuple[int, int]) -> None:
        if not (allowed_range[0] <= value <= allowed_range[1]):
            raise ValueError("value is not in allowed range")

    @staticmethod
    def make(
            token: str,
            allowed_range: Tuple[int, int],
            value_types: List[Type["Value"]]
    ) -> "Value":
        for ValueType in value_types:
            made_value = ValueType()
            if made_value.parse(token, allowed_range):
                return made_value

        logger.error(f"Invalid schedule value")
        raise ValueError("Invalid schedule value")


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
    _values: List[Value]
    _INNER_VALUE_TYPES = [NumberValue, EveryNthValue, RangeValue]

    def __init__(self):
        self._values = []

    def parse(self, token: str, allowed_range: Tuple[int, int]) -> bool:
        if re.match(r"^(.*?,)*.*?$", token):
            value_parts = token.split(",")
            self._values = [
                self.make(value_part, allowed_range, self._INNER_VALUE_TYPES)
                for value_part in value_parts
            ]
            return True
        return False

    def match(self, value: int) -> bool:
        return any(
            inner.match(value)
            for inner in self._values
        )


class Schedule:
    _AVAILABLE_VALUE_TYPES = [NumberValue, EveryNthValue, EveryTimeValue, RangeValue, MultipleValue]

    def __init__(self, time_string: str):
        parts = re.split(r"\s+", time_string)
        if len(parts) != 5:
            raise ValueError("Invalid time string format")

        self._minute = Value.make(parts[0], (0, 59), self._AVAILABLE_VALUE_TYPES)
        self._hour = Value.make(parts[1], (0, 23), self._AVAILABLE_VALUE_TYPES)
        self._day_of_month = Value.make(parts[2], (1, 31), self._AVAILABLE_VALUE_TYPES)
        self._month = Value.make(parts[3], (1, 12), self._AVAILABLE_VALUE_TYPES)
        self._day_of_week = Value.make(parts[4], (0, 7), self._AVAILABLE_VALUE_TYPES)

    def should_run(self, when: datetime = datetime.now()) -> bool:
        if not self._minute.match(when.minute):
            return False
        if not self._hour.match(when.hour):
            return False
        if not self._day_of_month.match(when.day):
            return False
        if not self._month.match(when.month):
            return False
        if not self._day_of_week.match(when.weekday() + 1):
            return False
        return True
