from enum import Enum
from base64 import decodebytes
from dataclasses import dataclass
from flask_mail import Message, Attachment


class Status(Enum):
    PENDING = 0
    FORWARDED = 1
    COMPLETED = 2


@dataclass
class EmailInfo:
    ticket_id: str
    client_name: str
    email_client: str
    channel: str
    type: str
    level: int
    status: Status
    description: str
    images: list


def generate_email(email: EmailInfo):
    header_info = f"Olá {email.client_name}"
    mid_info = ""
    if email.status == Status.PENDING:
        mid_info = "Sua reclamação está na nossa fila e ela será processada em breve."
    elif email.status == Status.FORWARDED:
        mid_info = "Sua reclamação está sendo analisada pelos nossos atendentes."
    else:
        mid_info = "Sua reclamação foi finalizada com sucesso."
    footer_info = (f"Informações da reclamação:\n\nCanal de comunicação: {email.channel}\n" +
                   f"Tipo da reclamação: {email.type}\nLevel (quanto maior mais prioritário): " +
                   f"{email.level}\nDescrição: {email.description}")
    title = f"Reclamação nº {email.ticket_id}"
    body = f"{header_info}\n\n{mid_info}\n{footer_info}"
    attachments = None
    if email.images:
        attachments = [
            Attachment(f'attachment_{i}.jpeg', 'image/jpeg', decodebytes(image.encode('ascii'))) for i, image in enumerate(email.images)
        ]

    return Message(title, [email.email_client], body, attachments=attachments)
