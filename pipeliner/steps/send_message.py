import logging
from fbchat import Client, Message

from pipeliner.steps.step import Step

logger = logging.getLogger(__name__)


class SendMessageFb(Step):
    def __init__(self, login: str, password: str, to_user_name: str):
        self._login = login
        self._password = password
        self._to_user_name = to_user_name
        self._client = None

    @property
    def client(self):
        if self._client is None:
            self._client = Client(
                self._login,
                self._password,
                user_agent="Mozilla/5.0 Pipeliner/0.1"
            )
        return self._client

    def perform(self, data: str) -> str:
        user = self.client.searchForUsers(self._to_user_name, limit=1)[0]  # ugly camelCase for method... pff
        logger.info(f"Sending message to facebook messenger as {self.client}")
        self.client.send(Message(text=data), thread_id=user.uid)
        return data
