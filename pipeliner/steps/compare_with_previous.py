import logging
from typing import Any

from pipeliner.steps_factory import HasStepsFactoryMixin, StepsFactory
from pipeliner.steps.step import Step

logger = logging.getLogger(__name__)


class CompareWithPrevious(Step, HasStepsFactoryMixin):
    _old_next_step: None or Step

    def __init__(self, factory: StepsFactory, when_same: dict, when_different: dict):
        super().__init__(factory)
        self._previous_data = None

        self._when_same = self._steps_factory.create_step(when_same)
        self._when_different = self._steps_factory.create_step(when_different)

    def perform(self, data: Any) -> Any:
        if self._previous_data is None:
            self._previous_data = data
            return data

        if self._previous_data != data:
            result = self._when_different.perform(data)
        else:
            result = self._when_same.perform(data)

        self._previous_data = data
        return result
