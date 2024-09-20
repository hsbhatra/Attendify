# RegAndAuth/tasks.py

from celery import shared_task
from email.message import EmailMessage
import ssl
import smtplib

@shared_task
def send_email(sender_email, sender_email_pass, receiver_email, subject, body):
    try:
        em = EmailMessage()
        em['From'] = sender_email
        em['To'] = receiver_email
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(sender_email, sender_email_pass)
            smtp.sendmail(sender_email, receiver_email, em.as_string())

    except Exception as e:
        print(f"Error sending email: {e}")
