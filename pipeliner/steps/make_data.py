import logging
import random
from typing import Any, List

from pipeliner.steps import Step

logger = logging.getLogger(__name__)


class ProduceText(Step):
    def __init__(self, text: str):
        self._text = text

    def perform(self, data: Any) -> str:
        logger.info(f"Producing text: {self._text}")
        return self._text


class PickRandomText(Step):
    def __init__(self, choices: List[str]):
        self._choices = choices

    def perform(self, data: Any) -> Any:
        picked = random.choice(self._choices)
        logger.info(f"Picked random text: {picked}")
        return picked
