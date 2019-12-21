from typing import Any

from pipeliner.steps import Step

import logging

logger = logging.getLogger(__name__)


class SayHello(Step):
    def perform(self, data: Any) -> Any:
        logger.info(f"Hello there! Got this: {data}")
        return data


class SayBye(Step):
    def perform(self, data: Any) -> Any:
        logger.info(f"Bye bye! Got this: {data}")
        return data
