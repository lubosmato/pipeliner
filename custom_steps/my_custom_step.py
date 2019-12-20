from pipeliner.steps import BasicStep

import logging


logger = logging.getLogger(__name__)


class SayHello(BasicStep):
    def perform(self, data: str) -> None:
        logger.info(f"Hello there!")
        super().perform(data)
