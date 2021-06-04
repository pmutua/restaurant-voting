
from django.core.mail import EmailMultiAlternatives


def send_credentials(subject, message, org_email):
    """Sends Email to User with Credentials."""
    subject, from_email, to = subject, 'philip@nouveta.tech', org_email
    text_content = message.get('text')
    html_content = message.get('html')

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
