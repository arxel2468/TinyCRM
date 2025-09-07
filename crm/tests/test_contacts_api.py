import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from crm.models import Contact

@pytest.fixture
def user(db):
    return get_user_model().objects.create_user(username="u1", password="pass12345")

@pytest.fixture
def client(user):
    client = APIClient()
    from rest_framework_simplejwt.tokens import RefreshToken
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    return client

def test_auth_required(db):
    c = APIClient()
    res = c.get("/api/contacts/")
    assert res.status_code == 401

def test_create_contact(client, db):
    res = client.post("/api/contacts/", {"name": "Alice", "email": "alice@example.com", "tags": "vip"})
    assert res.status_code == 201
    assert Contact.objects.filter(email="alice@example.com").exists()

def test_isolation_between_users(db):
    U = get_user_model()
    u1 = U.objects.create_user(username="u2", password="pass12345")
    u2 = U.objects.create_user(username="u3", password="pass12345")

    from rest_framework_simplejwt.tokens import RefreshToken
    c1 = APIClient(); c1.credentials(HTTP_AUTHORIZATION=f"Bearer {RefreshToken.for_user(u1).access_token}")
    c2 = APIClient(); c2.credentials(HTTP_AUTHORIZATION=f"Bearer {RefreshToken.for_user(u2).access_token}")

    res = c1.post("/api/contacts/", {"name": "Bob", "email": "bob@example.com"}, format="json")
    assert res.status_code == 201
    contact_id = res.json()["id"]

    res2 = c2.get(f"/api/contacts/{contact_id}/")
    assert res2.status_code in (403, 404)  # hidden from other users