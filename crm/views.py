from rest_framework import viewsets, permissions, filters
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import django_filters.rest_framework
from django.http import JsonResponse
from .models import Contact, Company, Deal
from .serializers import ContactSerializer, CompanySerializer, DealSerializer
from .filters import ContactFilter, CompanyFilter, DealFilter
from .pagination import StandardResultsPagination

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
	permission_classes=[IsAuthenticated] 
	
	def get(self, request): 
		return JsonResponse({"username": request.user.username, "email": request.user.email})