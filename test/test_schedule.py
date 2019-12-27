from typing import Set

import pytest
from datetime import datetime

from pipeliner.pipeline import Schedule
from pipeliner.schedule import NumberValue, EveryNthValue, EveryTimeValue, RangeValue, MultipleValue, Value


def match_values(value: Value, should_match: Set[int]):
    for i in range(100):
        if i in should_match:
            assert value.match(i)
        else:
            assert not value.match(i)


def test_schedule_value():
    value = NumberValue()
    assert value.parse("10", (0, 100))
    match_values(value, {10})

    value = EveryNthValue()
    assert value.parse("*/10", (0, 100))
    match_values(value, {0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100})

    value = EveryTimeValue()
    assert value.parse("*", (0, 100))
    match_values(value, set(range(101)))

    value = RangeValue()
    assert value.parse("10-20", (0, 100))
    match_values(value, {10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20})

    value = MultipleValue()
    assert value.parse("1,2,3,5-7,*/20,10", (0, 100))
    match_values(value, {0, 1, 2, 3, 5, 6, 7, 10, 20, 40, 60, 80, 100})


def test_schedule_time_format():
    with pytest.raises(ValueError):
        Schedule("hello there")

    with pytest.raises(ValueError):
        Schedule("* * * *")


def test_schedule_range():
    with pytest.raises(ValueError):
        Schedule("-1 -1 0 0 0")

    with pytest.raises(ValueError):
        Schedule("60 24 32 13 8")


def test_schedule():
    schedule = Schedule("* * * * *")
    assert schedule.should_run(datetime(2019, 12, 24, 11, 53, 25))

    schedule = Schedule("0 * * * *")
    assert not schedule.should_run(datetime(2019, 12, 24, 11, 53, 25))

    schedule = Schedule("0 0 1 1 *")
    assert schedule.should_run(datetime(2019, 1, 1, 0, 0, 0))

    schedule = Schedule("4 3 2 1 *")
    assert schedule.should_run(datetime(2019, 1, 2, 3, 4))

    schedule = Schedule("4 */3 2 1 *")
    assert schedule.should_run(datetime(2019, 1, 2, 3, 4))
    assert schedule.should_run(datetime(2019, 1, 2, 6, 4))
    assert schedule.should_run(datetime(2019, 1, 2, 9, 4))
    assert not schedule.should_run(datetime(2019, 1, 2, 4, 4))


def test_schedule_from_to():
    schedule = Schedule("* 9-14 * * *")
    assert not schedule.should_run(datetime(2019, 1, 1, 8, 0, 0))
    assert schedule.should_run(datetime(2019, 1, 1, 9, 0, 0))
    assert schedule.should_run(datetime(2019, 1, 1, 14, 0, 0))
    assert not schedule.should_run(datetime(2019, 1, 1, 15, 0, 0))


def test_schedule_multiple():
    schedule = Schedule("* 1,2,3 * * *")
    assert not schedule.should_run(datetime(2019, 1, 1, 0, 0, 0))
    assert schedule.should_run(datetime(2019, 1, 1, 1, 0, 0))
    assert schedule.should_run(datetime(2019, 1, 1, 2, 0, 0))
    assert schedule.should_run(datetime(2019, 1, 1, 3, 0, 0))
    assert not schedule.should_run(datetime(2019, 1, 1, 4, 0, 0))
