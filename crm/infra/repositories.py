from crm.models import Contact, Deal
from django.db.models import QuerySet


class ContactsRepo:
    @staticmethod
    def for_user(user) -> QuerySet[Contact]:
        return Contact.objects.filter(user=user)


class DealsRepo:
    @staticmethod
    def for_user(user) -> QuerySet[Deal]:
        return Deal.objects.select_related("company").filter(user=user)
