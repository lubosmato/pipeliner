import logging
from lxml import html

from pipeliner.steps.step import Step

logger = logging.getLogger(__name__)


class GetHtmlElementText(Step):
    def __init__(self, element_xpath: str):
        super().__init__()
        self._element_xpath = element_xpath

    def perform(self, data: str) -> str:
        root = html.fromstring(data)
        element_content = root.xpath(self._element_xpath)[0].text.strip()
        logger.info(f"Found content: {element_content}")
        return element_content
