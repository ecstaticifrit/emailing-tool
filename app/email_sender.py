import smtplib
from email.mime.text import MIMEText
from app.config import SMTP_HOST, SMTP_PORT, SMTP_EMAIL, SMTP_PASSWORD
import mailtrap as mt

client = mt.MailtrapClient(token="3d0f8962ea9141371c1275a48a7633b8")


def send_email(to_email, subject, html_body):

    mail = mt.Mail(
        sender=mt.Address(email="hello@demomailtrap.co", name="Mailtrap Test"),
        to=[mt.Address(email=to_email)],
        subject=subject,
        text=html_body,
        category="Integration Test",
    )

    response = client.send(mail)
    print(response)