from pipeliner.steps import BasicStep

import logging


logger = logging.getLogger(__name__)


class SayHello(BasicStep):
    def perform(self, data: str) -> None:
        logger.info(f"Hello there! Got this: {data}")
        super().perform(data)
