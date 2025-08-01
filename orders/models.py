from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('User'))
    first_name = models.CharField(_('First Name'), max_length=100)
    last_name = models.CharField(_('Last Name'), max_length=100)
    phone_number = models.CharField(_('Phone Number'), max_length=15)
    address = models.CharField(_('Address'), max_length=700)
    is_paid = models.BooleanField(_('Is Paid?'), default=False)
    order_notes = models.CharField(_('Order Notes'), max_length=700, blank=True)
    zarinpal_authority = models.CharField(_('Authority'), max_length=255, blank=True)
    zarinpal_ref_id = models.CharField(_('Reference ID'), max_length=150, blank=True)
    zarinpal_data = models.TextField(_('Zarinpal Data'), blank=True)
    datetime_created = models.DateTimeField(_('DateTime Created'), auto_now_add=True)
    datetime_modified = models.DateTimeField(_('DateTime Modified'), auto_now=True)

    def __str__(self):
        return f'Order {self.id}'

    def get_total_price(self):
        return sum(item.price * item.quantity for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()

    def __str__(self):
        return f'OrderItem {self.id}: {self.product} * {self.quantity} (price: {self.price})'