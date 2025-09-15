import pytest
from django.core import mail
from django.test.utils import override_settings
from crm.emails import send_digest_email

@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend", DEFAULT_FROM_EMAIL="TinyCRM test@example.com")
def test_send_digest_email(db):
    send_digest_email("user@example.com", "Subject", "Body", "col1,col2\nv1,v2\n")
    assert len(mail.outbox) == 1
    m = mail.outbox[0]
    assert m.subject == "Subject"
    assert m.to == ["user@example.com"]
    assert m.attachments and m.attachments[0][0] == "deals_digest.csv"
