import pytest
from django.contrib.auth import get_user_model
from crm.models import Company, Deal
from crm.services.digest import compute_deals_summary, deals_csv

def test_compute_summary_and_csv(db):
    U = get_user_model()
    u = U.objects.create_user(username="u1", password="pass")
    c = Company.objects.create(user=u,name="Acme")
    Deal.objects.create(user=u, company=c, title="A", amount=100, stage="new")
    Deal.objects.create(user=u, company=c, title="B", amount=200, stage="won")
    summary = compute_deals_summary(u, days=365)
    assert summary["totals"]["count"] == 2
    csv_text = deals_csv(u, days=365)
    assert "A" in csv_text and "B" in csv_text
