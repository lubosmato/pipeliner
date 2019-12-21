import logging
from pathlib import Path
from typing import Any

from pipeliner import config
from pipeliner.steps_factory import StepsFactory
from pipeliner.steps.step import Step

logger = logging.getLogger(__name__)


class CompareWithPrevious(Step):
    _old_next_step: None or Step

    def __init__(self, when_same: dict, when_different: dict):
        self._previous_data = None

        custom_steps_path = Path(config.config.get("custom_steps", "")).resolve()
        self._steps_factory = StepsFactory(custom_steps_path)

        self._when_same = self._steps_factory.create_step(when_same)
        self._when_different = self._steps_factory.create_step(when_different)

    def perform(self, data: Any) -> None:
        if self._previous_data is None:
            self._previous_data = data
            return data

        if self._previous_data != data:
            result = self._when_different.perform(data)
        else:
            result = self._when_same.perform(data)

        self._previous_data = data
        return result
