import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from crm.models import Company, Deal


@pytest.fixture
def auth_client(db):
    U = get_user_model()
    user = U.objects.create_user(username="u1", password="pass12345")
    from rest_framework_simplejwt.tokens import RefreshToken

    token = str(RefreshToken.for_user(user).access_token)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client, user


def test_deals_csv_export(auth_client, db):
    client, user = auth_client
    c = Company.objects.create(user=user, name="Acme")
    Deal.objects.create(user=user, company=c, title="D1", amount=100)
    r = client.get("/api/exports/deals.csv")
    assert r.status_code == 200
    assert r["Content-Type"] == "text/csv"
    assert "D1" in r.content.decode()
