import pytest
from datetime import datetime

from pipeliner.pipeline import Schedule


def test_schedule_value():
    value = Schedule.NumberValue()
    assert value.parse("10", (0, 100))

    assert not value.match(20)
    assert not value.match(11)
    assert value.match(10)

    value = Schedule.EveryNthValue()
    assert value.parse("*/10", (0, 100))
    assert value.match(20)
    assert not value.match(11)
    assert value.match(10)

    value = Schedule.EveryTimeValue()
    assert value.parse("*", (0, 100))
    assert value.match(1)
    assert value.match(2)
    assert value.match(3)

    value = Schedule.RangeValue()
    assert value.parse("10-20", (0, 100))
    assert not value.match(9)
    assert value.match(10)
    assert value.match(20)
    assert not value.match(21)

    value = Schedule.MultipleValue()
    assert value.parse("1,2,3", (0, 100))
    assert not value.match(0)
    assert value.match(1)
    assert value.match(2)
    assert value.match(3)
    assert not value.match(4)


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
