import logging
import random
from typing import Any, List

from pipeliner.steps import Step

logger = logging.getLogger(__name__)


class MakeTextData(Step):
    def __init__(self, data: str):
        self._data = data

    def perform(self, data: Any) -> str:
        logger.info(f"Making text data: {self._data}")
        return self._data


class PickRandomText(Step):
    def __init__(self, choices: List[str]):
        self._choices = choices

    def perform(self, data: Any) -> Any:
        picked = random.choice(self._choices)
        logger.info(f"Picked random text: {picked}")
        return picked
