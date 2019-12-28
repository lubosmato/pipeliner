import logging
from typing import Any

import requests

from pipeliner.steps.step import Step

logger = logging.getLogger(__name__)


class HttpDownload(Step):
    def __init__(self, url: str, headers: dict):
        super().__init__()
        self._url = url
        self._headers = headers

    def perform(self, data: Any) -> str:
        logger.info(f"Downloading {self._url} with headers {self._headers}")
        return requests.get(self._url, headers=self._headers).content
