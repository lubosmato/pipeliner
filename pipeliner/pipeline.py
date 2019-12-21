import logging
from typing import List

from pipeliner.steps.step import Step

logger = logging.getLogger(__name__)


class Pipeline:
    def __init__(self, name: str, schedule: str, steps: List[Step]):
        self._name = name
        self._schedule = schedule
        self._steps = steps
        self._has_failed = False

    def run(self) -> None:
        logger.info(f"Starting pipeline \"{self.name}\"")
        try:
            data = None
            for step in self._steps:
                logger.info(f"Pipeline \"{self.name}\", step {step}")
                data = step.perform(data)
            logger.info(f"Pipeline \"{self.name}\" has been finished")
        except Exception as e:
            logger.error(f"Pipeline \"{self.name}\" has failed: {e}")
            # TODO repeat (multiple times) when failed

    @property
    def name(self) -> str:
        return self._name

    @property
    def schedule(self) -> str:
        return self._schedule
