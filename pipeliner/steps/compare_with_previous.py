import logging
from pathlib import Path
from typing import Any

from pipeliner import config
from pipeliner.step_factory import StepFactory
from pipeliner.steps.step import BasicStep, Step

logger = logging.getLogger(__name__)


class CompareWithPrevious(BasicStep):
    _old_next_step: None or Step

    def __init__(self, when_same: dict, when_different: dict):
        super().__init__()
        self._old_value = None
        self._old_next_step = None

        custom_steps_path = Path(config.config.get("custom_steps", "")).resolve()
        self._step_factory = StepFactory(custom_steps_path)

        self._when_same = self._step_factory.create_step(when_same)
        self._when_different = self._step_factory.create_step(when_different)

    def set_next_step(self, step: Step) -> None:
        super().set_next_step(step)
        self._chain_branch_steps()

    def _chain_branch_steps(self):
        self._old_next_step = self._next_step
        self._when_same.set_next_step(self._next_step)
        self._when_different.set_next_step(self._next_step)

    def perform(self, data: Any) -> None:
        if self._old_value is None:
            self._next_step = self._old_next_step
        elif self._old_value != data:
            self._next_step = self._when_different
        else:
            self._next_step = self._when_same

        self._old_value = data
        super().perform(data)
