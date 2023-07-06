from dataclasses import dataclass
from flask_mail import Message


@dataclass
class EmailInfo:
    email_client: str
    channel: str
    type: str
    status: str
    description: str
    images: list


def generate_email(email: EmailInfo):
    body = ""
    return Message("", email.email_client, body)
