from datetime import datetime
from uuid import uuid4

from django.db import models

ORDER_CHOICES = (
    (1, 'Open'),
    (2, 'Hold'),
    (3, 'Closed'),
    (4, 'Canceled'),
    (5, 'Refunded')
)


class Order(models.Model):
    number = models.CharField(max_length=32)
    subtotal = models.FloatField()
    tax_total = models.FloatField()
    discount_total = models.FloatField()
    grand_total = models.FloatField()
    balance_remaining = models.FloatField(null=True, blank=True)
    open_date = models.DateTimeField(null=True, blank=True)
    hold_date = models.DateTimeField(null=True, blank=True)
    close_date = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField(choices=ORDER_CHOICES)
    description = models.CharField(null=True, blank=True, max_length=128)
    customer = models.ForeignKey('employees.Customer', related_name="orders", null=True, blank=True)
    emp_open = models.ForeignKey('employees.Employee', related_name="order_as_open", null=True, blank=True)
    emp_close = models.ForeignKey('employees.Employee', related_name="order_as_close", null=True, blank=True)
    discount_orders = models.FloatField(null=True, blank=True)
    terminal_id = models.IntegerField(null=True, blank=True, default=-1)
    shift = models.ForeignKey('payments.Shift', blank=True, null=True)

    def __unicode__(self):
        return u"Order #%s" % self.id

    def save(self, **kwargs):
        q = Order.objects.values_list('id', flat=True).order_by('-id')[:1]
        if len(q):
            self.number = str(self.id) if self.id else str(int(q.get()) + 1)
        else:
            self.number = 1
        return super(Order, self).save(**kwargs)

    def get_next(self):
        next_item = Order.objects.filter(id__gt=self.id).order_by('id').first()
        return next_item

    def get_prev(self):
        prev = Order.objects.filter(id__lt=self.id).order_by('-id').first()
        return prev

    def discount_items(self):
        # return self.items  # TBD?
        return sum(self.items.values_list('discount', flat=True))

    def get_custom_items(self):
        items = []
        items = self.items.filter(product_id=-1).exclude(void_status=1)
        return items


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items")
    name = models.CharField(max_length=64)
    price = models.FloatField()
    cost = models.FloatField()
    discount = models.FloatField()
    tax = models.FloatField()
    void_status = models.IntegerField(blank=True, null=True)
    employee = models.ForeignKey('employees.Employee', related_name="employee_order_items", null=True, blank=True)
    product = models.ForeignKey('products.Product', related_name="order_items", null=True, blank=True)
    # quantity = models.IntegerField()
    quantity = models.FloatField(default=0.0)
    terminal_id = models.IntegerField(null=True, blank=True, default=-1)
    create_at = models.DateTimeField(default=datetime.now(), blank=True, null=True)
    voided_at = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.name

    def get_modifiers(self):
        return self.modifiers.filter(void_status=False)


class OrderOption(models.Model):
    item = models.ForeignKey(OrderItem, related_name='options')
    name = models.CharField(max_length=64)
    cost = models.FloatField()
    price = models.FloatField()
    product = models.ForeignKey('products.Product', related_name='options')


class OrderModifier(models.Model):
    item = models.ForeignKey(OrderItem, related_name="modifiers")
    name = models.CharField(max_length=64)
    cost = models.FloatField()
    price = models.FloatField()
    oryginal = models.ForeignKey('products.Modifier', related_name='ordered')
    group = models.ForeignKey('products.ModifierGroup', related_name='modifiers_in_orders')
    void_status = models.BooleanField(default=False)


class SharedOrder(models.Model):
    order = models.ForeignKey(Order)
    identifier = models.CharField(max_length=512, default=uuid4)
