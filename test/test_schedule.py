import pytest
from datetime import datetime

from pipeliner.pipeline import Schedule


def test_schedule_value():
    value = Schedule.NumberValue(10)
    assert not value.match(20)
    assert not value.match(11)
    assert value.match(10)

    value = Schedule.EveryNthValue(10)
    assert value.match(20)
    assert not value.match(11)
    assert value.match(10)

    value = Schedule.RangeValue(10, 20)
    assert not value.match(9)
    assert value.match(10)
    assert value.match(20)
    assert not value.match(21)


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
