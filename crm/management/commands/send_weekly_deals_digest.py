from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from crm.services.digest import compute_deals_summary, deals_csv
from crm.emails import send_digest_email


class Command(BaseCommand):
    help = "Send weekly deals digest (CSV + summary) to users with an email"

    def handle(self, *args, **options):
        U = get_user_model()
        users = U.objects.filter(is_active=True).exclude(email="")
        count = 0
        for u in users:
            summary = compute_deals_summary(u, days=7)
            csv_text = deals_csv(u, days=7)
            subject = f"TinyCRM — Weekly deals digest ({(summary['totals']['count'] or 0) if summary['totals'] else 0} deals)"
            body = f"Hi {u.username},\n\nHere’s your weekly deals summary:\n{summary}\n\n— TinyCRM"
            try:
                send_digest_email(u.email, subject, body, csv_text)
                count += 1
            except Exception as e:
                self.stderr.write(f"Failed to email {u.email}: {e}")
        self.stdout.write(f"Weekly digest attempted for {count} user(s).")
