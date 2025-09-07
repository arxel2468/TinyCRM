from django.db import models
from django.conf import settings

# Create your models here.
class Contact(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="contacts")
    name = models.CharField(max_length=120)
    email = models.EmailField()
    tags = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
    	constraints = [
    		models.UniqueConstraint(fields=["user", "email"], name="uniq_user_email"),
    	]
    	ordering = ["-updated_at"]

    def __str__(self):
    	return f"{self.name} <{self.email}"

