import copy
import logging
from typing import List, Any

from pipeliner.schedule import Schedule
from pipeliner.steps.step import Step

logger = logging.getLogger(__name__)


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
            logger.info(f"Pipeline \"{self.name}\" has finished.")
        except Exception as e:
            logger.error(f"Pipeline \"{self.name}\" has failed because {e}")
            raise e

    def _perform_step(self, step: Step) -> None:
        logger.info(f"Starting step {step} from \"{self.name}\".")

        last_exception = None
        for _ in range(self.STEP_REPEAT_TRY_COUNT):
            try:
                copied_data = copy.deepcopy(self._current_data)
                self._current_data = step.perform(copied_data)
                logger.info(f"Finished step {step} from \"{self.name}\".")
                return
            except Exception as e:
                logger.warning(f"Failed step {step} from \"{self.name}\". Retrying...")
                last_exception = e

        if last_exception:
            logger.error(f"Step {step} from \"{self.name}\" failed too many times.")
            raise last_exception

    @property
    def name(self) -> str:
        return self._name

    @property
    def schedule(self) -> Schedule:
        return self._schedule
