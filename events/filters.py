import django_filters as filters
from .models import Event
from rest_framework.filters import SearchFilter


class EventFilter(filters.FilterSet):
    date_from = filters.IsoDateTimeFilter(field_name="date", lookup_expr="gte")
    date_to = filters.IsoDateTimeFilter(field_name="date", lookup_expr="lte")

    class Meta:
        model = Event
        fields = []


class PostgresSearchFilter(SearchFilter):
    search_param = "search"
