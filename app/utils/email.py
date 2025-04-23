#Backend/app/utils/email.py
from flask_mail import Message

from ..extensions import mail


def send_verification_email(email, code):
    msg = Message(
        "Your Code",
        sender=("Giv and Grow", "baraa.shellbaya@gmail.com"),
        recipients=[email],
    )
    msg.body = f"Your code is: {code}\nUse this code to verify your email or reset your password."
    mail.send(msg)