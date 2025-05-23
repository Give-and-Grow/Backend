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

    
def send_invitation_email(user_email, opportunity_title, organization_name, join_link):
    msg = Message(
        f"Invitation to join: {opportunity_title}",
        sender=("Giv and Grow", "baraa.shellbaya@gmail.com"),
        recipients=[user_email],
    )
    msg.body = (
        f"Hello,\n\n"
        f"You have been invited by {organization_name} to participate in the opportunity: {opportunity_title}.\n"
        f"Click the link below to view or apply:\n{join_link}\n\n"
        f"If you're not interested, feel free to ignore this email.\n\n"
        f"Best regards,\n"
        f"The Giv and Grow Team"
    )
    mail.send(msg)    