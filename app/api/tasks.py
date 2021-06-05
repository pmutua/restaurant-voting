
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

SENDER_EMAIL = settings.SENDGRID_SENDER_EMAIL


def send_credentials(subject, message, org_email):
    """Sends Email to User with Credentials."""
    subject, from_email, to = subject, SENDER_EMAIL, org_email
    text_content = message.get('text')
    html_content = message.get('html')

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
