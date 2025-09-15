import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from crm.models import Company, Deal

@pytest.fixture
def auth_client(db):
    U = get_user_model()
    u = U.objects.create_user(username="u1", password="pass12345")
    from rest_framework_simplejwt.tokens import RefreshToken
    c = APIClient(); c.credentials(HTTP_AUTHORIZATION=f"Bearer {RefreshToken.for_user(u).access_token}")
    return c, u

def test_deals_stats(auth_client, db):
    c, u = auth_client
    cmp = Company.objects.create(user=u, name="Acme")
    Deal.objects.create(user=u, company=cmp, title="A", amount=100, stage="new")
    Deal.objects.create(user=u, company=cmp, title="B", amount=200, stage="won")
    r = c.get("/api/stats/deals/?days=365")
    assert r.status_code == 200
    data = r.json()
    assert "totals" in data and data["totals"]["count"] == 2
