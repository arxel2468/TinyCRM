from rest_framework import serializers
from .models import Contact, Company, Deal


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ["id", "name", "email", "tags", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name", "website", "created_at"]
        read_only_fields = ["id", "created_at"]


class DealSerializer(serializers.ModelSerializer):
    company_name = serializers.ReadOnlyField(source="company.name")

    class Meta:
        model = Deal
        fields = [
            "id",
            "title",
            "amount",
            "stage",
            "close_date",
            "company",
            "company_name",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    # Restrict the company field to the current user's companies
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            from .models import Company

            self.fields["company"].queryset = Company.objects.filter(user=request.user)
