import logging
import smtplib
import ssl
from email.header import Header
from email.mime.text import MIMEText
from typing import List

from pipeliner.steps.step import Step

logger = logging.getLogger(__name__)


class SendEmailTls(Step):
    def __init__(self,
                 smtp_host: str,
                 smtp_port: int,
                 login: str,
                 password: str,
                 from_email: str,
                 to_emails: List[str],
                 subject: str):
        super().__init__()
        self._smtp_host = smtp_host
        self._smtp_port = smtp_port
        self._login = login
        self._password = password
        self._from_email = from_email
        self._to_emails = to_emails
        self._subject = subject

    def perform(self, data: str) -> str:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        with smtplib.SMTP(self._smtp_host, self._smtp_port) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(self._login, self._password)

            message = MIMEText(data, "html", "utf-8")
            message["Subject"] = Header(self._subject, "utf-8")
            message["From"] = self._from_email
            message["To"] = ",".join(self._to_emails)

            server.sendmail(self._from_email, self._to_emails, message.as_string().encode("ascii"))

        logger.info("Email was sent successfully")
        return data


class SendEmailSsl(Step):
    def __init__(self,
                 smtp_host: str,
                 smtp_port: int,
                 login: str,
                 password: str,
                 from_email: str,
                 to_emails: List[str],
                 subject: str):
        super().__init__()
        self._smtp_host = smtp_host
        self._smtp_port = smtp_port
        self._login = login
        self._password = password
        self._from_email = from_email
        self._to_emails = to_emails
        self._subject = subject

    def perform(self, data: str) -> str:
        with smtplib.SMTP_SSL(self._smtp_host, self._smtp_port) as server:
            server.ehlo()
            server.login(self._login, self._password)

            message = MIMEText(data, "html", "utf-8")
            message["Subject"] = Header(self._subject, "utf-8")
            message["From"] = self._from_email
            message["To"] = ",".join(self._to_emails)

            server.sendmail(self._from_email, self._to_emails, message.as_string().encode("ascii"))

        logger.info("Email was sent successfully")
        return data
