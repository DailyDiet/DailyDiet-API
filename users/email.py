from flask_mail import Message

from extentions import mail


def send_email(to, subject, template):
    msg = Message(
        subject=subject,
        recipients=[to],
        html=template
    )
    mail.send(msg)
