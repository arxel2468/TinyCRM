from rest_framework import viewsets, permissions, filters
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import django_filters.rest_framework
from django.http import HttpResponse
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta
from .models import Contact, Company, Deal
from .serializers import ContactSerializer, CompanySerializer, DealSerializer
from .filters import ContactFilter, CompanyFilter, DealFilter
from .pagination import StandardResultsPagination
import csv
from io import StringIO


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return getattr(obj, "user_id", None) == request.user.id


class OwnedModelViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        django_filters.rest_framework.DjangoFilterBackend,
    ]
    pagination_class = StandardResultsPagination

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ContactViewSet(OwnedModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    filterset_class = ContactFilter
    search_fields = ["name", "email", "tags"]
    ordering_fields = ["name", "email", "created_at", "updated_at"]
    ordering = ["-updated_at"]


class CompanyViewSet(OwnedModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filterset_class = CompanyFilter
    search_fields = ["name"]
    ordering_fields = ["name", "created_at"]


class DealViewSet(OwnedModelViewSet):
    queryset = Deal.objects.select_related("company").all()
    serializer_class = DealSerializer
    filterset_class = DealFilter
    search_fields = ["title", "company__name"]
    ordering_fields = ["amount", "updated_at", "close_date"]


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {"username": request.user.username, "email": request.user.email}
        )


class DealsExportCSV(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = (
            Deal.objects.filter(user=request.user)
            .select_related("company")
            .order_by("-updated_at")
        )
        # Optional filters
        min_amount = request.GET.get("min_amount")
        if min_amount:
            qs = qs.filter(amount__gte=min_amount)

        buffer = StringIO()
        writer = csv.writer(buffer)
        writer.writerow(
            [
                "id",
                "title",
                "amount",
                "stage",
                "company",
                "close_date",
                "created_at",
                "updated_at",
            ]
        )
        for d in qs.iterator():
            writer.writerow(
                [
                    d.id,
                    d.title,
                    d.amount,
                    d.stage,
                    d.company.name,
                    d.close_date or "",
                    d.created_at,
                    d.updated_at,
                ]
            )

        resp = HttpResponse(buffer.getvalue(), content_type="text/csv")
        resp["Content-Disposition"] = 'attachment; filename="deals.csv"'
        return resp


class DealsStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            days = int(request.GET.get("days", "30"))
        except ValueError:
            days = 30
        since = timezone.now() - timedelta(days=days)
        qs = Deal.objects.filter(user=request.user, created_at__gte=since)
        by_stage = list(
            qs.values("stage")
            .annotate(count=Count("id"), amount=Sum("amount"))
            .order_by("stage")
        )
        totals = qs.aggregate(count=Count("id"), amount=Sum("amount"))
        return Response({"range_days": days, "by_stage": by_stage, "totals": totals})
