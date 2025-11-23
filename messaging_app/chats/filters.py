import django_filters
from .models import Message


class MessageFilter(django_filters.FilterSet):
    # Filter by conversation participant (user ID)
    participant = django_filters.NumberFilter(field_name="conversation__participants__id", lookup_expr="exact")

    # Filter by date range
    start_date = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr="gte")
    end_date = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr="lte")

    class Meta:
        model = Message
        fields = ["participant", "start_date", "end_date"]
