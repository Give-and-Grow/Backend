#Backend/app/utils/email.py
from flask_mail import Message
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ..extensions import mail
import os

def send_verification_email(email, code):
    msg = Message(
        "Your Code",
        sender=("Give and Grow", "baraa.shellbaya@gmail.com"),
        recipients=[email],
    )
    msg.body = f"Your code is: {code}\nUse this code to verify your email or reset your password."
    mail.send(msg)

    
def send_invitation_email(user_email, opportunity_title, organization_name, join_link):
    msg = Message(
        f"Invitation to join: {opportunity_title}",
        sender=("Give and Grow", "baraa.shellbaya@gmail.com"),
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

def send_insufficient_hours_email(user_email, user_name, opportunity_title, attended_hours, required_hours):
    msg = Message(
        "Volunteer Certificate - Not Eligible",
        sender=("Give and Grow", "baraa.shellbaya@gmail.com"),
        recipients=[user_email],
    )
    msg.body = (
        f"Dear {user_name},\n\n"
        f"Thank you for your participation in \"{opportunity_title}\". Unfortunately, your attendance "
        f"was below the minimum required hours.\n\n"
        f"Hours Attended: {attended_hours}\n"
        f"Required Hours: {required_hours}\n\n"
        f"For this reason, a certificate cannot be issued.\n\n"
        f"Kind regards,\n"
        f"The Giv and Grow Team"
    )
    mail.send(msg)

import os
from flask_mail import Message

def send_certificate_email(user_email, user_name, opportunity_title, pdf_bytes, filename):
    msg = Message(
        subject="Your Volunteer Certificate",
        sender=("Give and Grow", "baraa.shellbaya@gmail.com"),
        recipients=[user_email],
    )

    html_body = (
        f"<p><img src='cid:title_image'></p>"
        f"<p><img src='cid:congrats_image'></p>"
        f"<p>Dear {user_name},</p>"
        f"<p>Congratulations! You have successfully completed the opportunity <strong>{opportunity_title}</strong>.</p>"
        f"<p>Please find your certificate attached.</p>"
        f"<p>Best regards,<br>The Give and Grow Team</p>"
    )

    plain_body = (
        f"Dear {user_name},\n\n"
        f"Congratulations! You have successfully completed the opportunity \"{opportunity_title}\".\n"
        f"Please find your certificate attached.\n\n"
        f"Best regards,\n"
        f"The Give and Grow Team"
    )

    msg.body = plain_body
    msg.html = html_body

    # إرفاق الشهادة PDF
    msg.attach(filename, "application/pdf", pdf_bytes.read())

    # إرفاق الصورة كمرفق داخلي داخل الإيميل
    current_dir = os.path.dirname(__file__)
    # إرفاق الصورة الأولى (title image)
    title_image_path = os.path.join(current_dir, "assets", "title_img.png")
    with open(title_image_path, "rb") as img_file:
        title_image_data = img_file.read()
        msg.attach("title_img.png", "image/png", title_image_data, headers={"Content-ID": "<title_image>"})


    image_path = os.path.join(current_dir, "assets", "congrats_img.gif")
    with open(image_path, "rb") as img_file:
        image_data = img_file.read()
        msg.attach("congrats_img.gif", "image/gif", image_data, headers={"Content-ID": "<congrats_image>"})


    # إرسال الإيميل
    mail.send(msg)
