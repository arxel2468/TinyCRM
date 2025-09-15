from django.core.mail import EmailMessage
from django.conf import settings


def send_digest_email(to_email, subject, body, csv_text):
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to_email],
    )
    email.attach("deals_digest.csv", csv_text, "text/csv")
    email.send(fail_silently=False)
