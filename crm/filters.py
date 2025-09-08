import django_filters
from .models import Contact


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
