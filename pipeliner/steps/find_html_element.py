import logging
from lxml import html

from pipeliner.steps.step import BasicStep

logger = logging.getLogger(__name__)


class FindHtmlElement(BasicStep):
    def __init__(self, element_xpath: str):
        super().__init__()
        self._element_xpath = element_xpath

    def perform(self, data: str) -> None:
        logger.info(f"Got this data {data}")
        super().perform(data)
