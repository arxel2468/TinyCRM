import django_filters
from .models import Contact, Company, Deal


class ContactFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    email = django_filters.CharFilter(lookup_expr="icontains")
    tags = django_filters.CharFilter(method="filter_tags")
    created_after = django_filters.IsoDateTimeFilter(
        field_name="created_at", lookup_expr="gte"
    )
    created_before = django_filters.IsoDateTimeFilter(
        field_name="created_at", lookup_expr="lte"
    )

    def filter_tags(self, queryset, name, value):
        # Comma-separated search: tags=vip,new will match both
        tokens = [t.strip() for t in value.split(",") if t.strip()]
        for t in tokens:
            queryset = queryset.filter(tags__icontains=t)
        return queryset

    class Meta:
        model = Contact
        fields = ["name", "email", "tags", "created_after", "created_before"]

class CompanyFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Company
        fields = ["name"]


class DealFilter(django_filters.FilterSet):
    min_amount = django_filters.NumberFilter(field_name="amount", lookup_expr="gte")
    max_amount = django_filters.NumberFilter(field_name="amount", lookup_expr="lte")
    stage = django_filters.CharFilter(field_name="stage")
    close_before = django_filters.DateFilter(field_name="close_date", lookup_expr="lte")
    close_after = django_filters.DateFilter(field_name="close_date", lookup_expr="gte")

    class Meta:
        model = Deal
        fields = ["stage"]

