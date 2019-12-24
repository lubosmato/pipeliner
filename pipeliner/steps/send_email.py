import logging
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from pipeliner.steps.step import Step

logger = logging.getLogger(__name__)


class SendEmailTls(Step):
    def __init__(self, smtp_host: str, smtp_port: int, login: str, password: str, from_email: str, to_email: str, subject: str):
        super().__init__()
        self._smtp_host = smtp_host
        self._smtp_port = smtp_port
        self._login = login
        self._password = password
        self._from_email = from_email
        self._to_email = to_email
        self._subject = subject

    def perform(self, data: str) -> str:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        with smtplib.SMTP(self._smtp_host, self._smtp_port) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(self._login, self._password)

            message = MIMEMultipart("alternative")
            message["Subject"] = self._subject
            message["From"] = self._from_email
            message["To"] = self._to_email

            message.attach(MIMEText(data, "plain"))
            message.attach(MIMEText(data, "html"))

            server.sendmail(self._from_email, self._to_email, message.as_string())

        logger.info("Email was sent successfully")
        return data


class SendEmailSsl(Step):
    def __init__(self, smtp_host: str, smtp_port: int, login: str, password: str, from_email: str, to_email: str, subject: str):
        super().__init__()
        self._smtp_host = smtp_host
        self._smtp_port = smtp_port
        self._login = login
        self._password = password
        self._from_email = from_email
        self._to_email = to_email
        self._subject = subject

    def perform(self, data: str) -> str:
        with smtplib.SMTP_SSL(self._smtp_host, self._smtp_port) as server:
            server.ehlo()
            server.login(self._login, self._password)

            message = MIMEMultipart("alternative")
            message["Subject"] = self._subject
            message["From"] = self._from_email
            message["To"] = self._to_email

            message.attach(MIMEText(data, "plain"))
            message.attach(MIMEText(data, "html"))

            server.sendmail(self._from_email, self._to_email, message.as_string())

        logger.info("Email was sent successfully")
        return data
