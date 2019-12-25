import logging
from fbchat import Client, Message

from pipeliner.steps.step import Step

logger = logging.getLogger(__name__)


class SendMessageFb(Step):
    def __init__(self, login: str, password: str, to_user_name: str):
        self._login = login
        self._password = password
        self._to_user_name = to_user_name

    def perform(self, data: str) -> str:
        client = Client(self._login, self._password)
        user = client.searchForUsers(self._to_user_name, limit=1)[0]  # ugly camelCase for method... pff
        logger.info(f"Sending message to facebook messenger as {client}")
        client.send(Message(text=data), thread_id=user.uid)
        client.logout()
        return data
