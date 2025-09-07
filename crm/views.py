from rest_framework import viewsets, permissions
from .models import Contact
from .serializers import ContactSerializer

class IsOwner(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		return obj.user_id == request.user.id

class ContactViewSet(viewsets.ModelViewSet):	
	serializer_class = ContactSerializer
	permission_classes = [permissions.IsAuthenticated, IsOwner]

	filterset_fields = ["email"]
	search_fields = ["name", "email", "tags"]
	ordering_fields = ["name", "email", "created_at", "updated_at"]

	def get_queryset(self):
		return Contact.objects.filter(user=self.request.user)

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

