import logging
from typing import Any

from pipeliner.steps.step import BasicStep

logger = logging.getLogger(__name__)


class CompareWithPrevious(BasicStep):
    def __init__(self):
        super().__init__()
        self._old_value = None

    def perform(self, data: Any) -> None:
        if self._old_value is None:
            super().perform((False, data))
            return

        is_different = self._old_value != data
        self._old_value = data
        super().perform((is_different, data))
