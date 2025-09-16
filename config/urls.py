import os
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib import admin
from django.urls import path, include
from rest_framework.views import APIView
from rest_framework.response import Response
from crm.management.commands.send_weekly_deals_digest import Command as DigestCmd
from rest_framework.routers import DefaultRouter
from crm.views import (
    ContactViewSet,
    CompanyViewSet,
    DealViewSet,
    MeView,
    DealsExportCSV,
    DealsStatsView,
    ContactsImportCSV,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from crm.auth_views import ThrottledTokenObtainPairView, ThrottledTokenRefreshView
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView


class RunDigestView(APIView):
    authentication_classes = []  # no auth, we use a header secret
    permission_classes = []

    def post(self, request):
        secret = request.headers.get("X-CRON-KEY")
        expected = os.getenv("CRON_SECRET")
        if not expected or secret != expected:
            return HttpResponseForbidden("Forbidden")
        DigestCmd().handle()
        return Response({"status": "ok"})


router = DefaultRouter()
router.register(r"contacts", ContactViewSet, basename="contact")
router.register(r"companies", CompanyViewSet, basename="company")
router.register(r"deals", DealViewSet, basename="deal")

urlpatterns = [
    path("admin /", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/", include(router.urls)),
    path("api/me/", MeView.as_view()),
    path("api/exports/deals.csv", DealsExportCSV.as_view(), name="deals_export_csv"),
    path("api/stats/deals/", DealsStatsView.as_view(), name="deals_stats"),
    path("healthz", lambda r: HttpResponse("ok")),
    path("api/admin/run-weekly-digest", RunDigestView.as_view()),
    path(
        "api/token/", ThrottledTokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(
        "api/token/refresh/", ThrottledTokenRefreshView.as_view(), name="token_refresh"
    ),
    path("api/imports/contacts/", ContactsImportCSV.as_view(), name="contacts_import"),
]
