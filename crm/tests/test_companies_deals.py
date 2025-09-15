import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


@pytest.fixture
def auth_client(db):
    U = get_user_model()
    user = U.objects.create_user(username="u1", password="pass12345")
    from rest_framework_simplejwt.tokens import RefreshToken

    token = str(RefreshToken.for_user(user).access_token)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client, user


@pytest.fixture
def other_client(db):
    U = get_user_model()
    user = U.objects.create_user(username="u2", password="pass12345")
    from rest_framework_simplejwt.tokens import RefreshToken

    token = str(RefreshToken.for_user(user).access_token)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client, user


def test_company_and_deal_crud(auth_client, db):
    client, _ = auth_client
    # Create company
    r = client.post(
        "/api/companies/",
        {"name": "Acme", "website": "https://acme.test"},
        format="json",
    )
    assert r.status_code == 201
    company_id = r.json()["id"]

    # Create deal
    r = client.post(
        "/api/deals/",
        {
            "title": "First Deal",
            "amount": "999.99",
            "stage": "new",
            "company": company_id,
        },
        format="json",
    )
    assert r.status_code == 201

    # List deals with filter + ordering
    r = client.get("/api/deals/?min_amount=500&ordering=-amount")
    assert r.status_code == 200
    assert r.json()["count"] == 1


def test_cannot_use_someone_elses_company(auth_client, other_client, db):
    client1, _ = auth_client
    client2, _ = other_client

    # User1 creates a company
    r = client1.post("/api/companies/", {"name": "User1Co"}, format="json")
    assert r.status_code == 201
    company_id = r.json()["id"]

    # User2 tries to create a deal referencing User1's company -> should be 400
    r = client2.post(
        "/api/deals/",
        {"title": "Bad Deal", "amount": "10.00", "company": company_id},
        format="json",
    )
    assert r.status_code == 400

    # User2 shouldn't see User1's company
    r = client2.get(f"/api/companies/{company_id}/")
    assert r.status_code in (403, 404)
