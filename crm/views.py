import django_filters
from rest_framework import viewsets, permissions, filters
from .models import Contact
from .serializers import ContactSerializer
from .filters import ContactFilter


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user_id == request.user.id


class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    filterset_class = ContactFilter
    filter_backends = [  # Explicit is fine; we can rely on settings too
        filters.SearchFilter,
        filters.OrderingFilter,
        django_filters.rest_framework.DjangoFilterBackend,
    ]
    search_fields = ["name", "email", "tags"]
    ordering_fields = ["name", "email", "created_at", "updated_at"]
    ordering = ["-updated_at"]

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
