from email.message import EmailMessage
import ssl
import smtplib

def send_email(sender_email, sender_email_pass, receiver_email, subject, body):
    """
    Sends an email using SMTP_SSL (used for OTP and notifications).
    Returns True if sent successfully, False otherwise.
    """
    try:
        em = EmailMessage()
        em['From'] = sender_email
        em['To'] = receiver_email
        em['subject'] = subject
        em.set_content(body)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(sender_email, sender_email_pass)
            smtp.sendmail(sender_email, receiver_email, em.as_string())
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
