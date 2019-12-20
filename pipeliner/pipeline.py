import logging

from pipeliner.steps.step import Step

logger = logging.getLogger(__name__)


class Pipeline:
    def __init__(self, name: str, schedule: str, beginning_step: Step):
        self._name = name
        self._schedule = schedule
        self._beginning_step = beginning_step

    def run(self) -> None:
        logger.info(f"Starting pipeline \"{self.name}\"")
        try:
            self._beginning_step.perform(None)
            logger.info(f"Pipeline \"{self.name}\" has been finished")
        except Exception as e:
            logger.error(f"Pipeline \"{self.name}\" has failed: {e}")

    @property
    def name(self) -> str:
        return self._name

    @property
    def schedule(self) -> str:
        return self._schedule
