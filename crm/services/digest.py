from datetime import timedelta
from django.utils import timezone
from django.db.models import Count, Sum
from io import StringIO
import csv
from crm.models import Deal


def compute_deals_summary(user, days=7):
    since = timezone.now() - timedelta(days=days)
    qs = Deal.objects.filter(user=user, created_at__gte=since)
    by_stage = list(
        qs.values("stage")
        .annotate(count=Count("id"), amount=Sum("amount"))
        .order_by("stage")
    )
    totals = qs.aggregate(count=Count("id"), amount=Sum("amount"))
    return {"range_days": days, "by_stage": by_stage, "totals": totals}


def deals_csv(user, days=7):
    since = timezone.now() - timedelta(days=days)
    qs = (
        Deal.objects.filter(user=user, created_at__gte=since)
        .select_related("company")
        .order_by("-updated_at")
    )
    buf = StringIO()
    w = csv.writer(buf)
    w.writerow(
        ["id", "title", "amount", "stage", "company", "close_date", "created_at"]
    )
    for d in qs.iterator():
        w.writerow(
            [
                d.id,
                d.title,
                d.amount,
                d.stage,
                d.company.name,
                d.close_date or "",
                d.created_at,
            ]
        )
    return buf.getvalue()
