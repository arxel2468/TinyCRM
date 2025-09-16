import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.fixture
def auth_client(db):
    U = get_user_model()
    u = U.objects.create_user(username="u1", password="pass12345")
    from rest_framework_simplejwt.tokens import RefreshToken

    c = APIClient()
    c.credentials(HTTP_AUTHORIZATION=f"Bearer {RefreshToken.for_user(u).access_token}")
    return c, u


def test_contacts_import_csv(auth_client, db):
    c, _ = auth_client
    csv_bytes = b"name,email,tags\nAlice,alice@example.com,vip\nBad,not-an-email,\n"
    f = SimpleUploadedFile("contacts.csv", csv_bytes, content_type="text/csv")
    r = c.post("/api/imports/contacts/", {"file": f})
    assert r.status_code == 200
    body = r.json()
    assert body["created"] == 1
    assert body["skipped"] == 1
