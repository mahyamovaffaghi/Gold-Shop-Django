import django_filters
from order.models import ItemOrder

class OrderPaidFilter(django_filters.FilterSet):
    order_paid = django_filters.BooleanFilter(field_name='order__order_paid', label='پرداخت شده؟')

    class Meta:
        model = ItemOrder
        fields = ['order_paid']

