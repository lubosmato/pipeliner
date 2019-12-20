import logging

import requests

from pipeliner.steps.step import BasicStep

logger = logging.getLogger(__name__)


class HttpDownload(BasicStep):
    def __init__(self, url: str, headers: dict):
        super().__init__()
        self._url = url
        self._headers = headers

    def perform(self, data: str) -> None:
        logger.info(f"Downloading {self._url} with headers {self._headers}")
        super().perform(requests.get(self._url, headers=self._headers).content)
