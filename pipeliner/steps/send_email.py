import logging
import smtplib
from email.mime.text import MIMEText
from typing import Any

from pipeliner.steps.step import BasicStep, Step

logger = logging.getLogger(__name__)


class SendEmail(BasicStep):
    _old_next_step: None or Step

    def __init__(self, smtp_host: str, smtp_port: int, login: str, password: str, from_email: str, to_email: str, subject: str):
        super().__init__()
        self._smtp_host = smtp_host
        self._smtp_port = smtp_port
        self._login = login
        self._password = password
        self._from_email = from_email
        self._to_email = to_email
        self._subject = subject

    def perform(self, data: Any) -> None:
        try:
            with smtplib.SMTP_SSL(self._smtp_host, self._smtp_port) as server:
                server.ehlo()
                server.login(self._login, self._password)

                message = MIMEText(data)
                message["Subject"] = self._subject
                message["From"] = self._from_email
                message["To"] = self._to_email

                server.sendmail(self._from_email, self._to_email, message.as_string())

            logger.info("Email was sent successfully")
        except Exception as e:
            logger.error(f"Could not send an email because {e}")

        super().perform(data)
