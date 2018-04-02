import collections
from django.db import models
from django.utils.translation import ugettext_lazy as _


class SpecialPricesManager(models.Manager):
    def get_for_user(self, events, user):
        ratings = self.filter(event__in=[event.id for event in events],
                              user=user)
        rating_dict = collections.defaultdict(lambda: None)
        for rating in ratings:
            rating_dict[rating.event_id] = rating
        return rating_dict


class CustomerGroup(models.Model):
    name = models.CharField(verbose_name=_('Group Name'), max_length=125)
    archived = models.BooleanField(default=False)

    # meanwhile  the best way will be do % dicount for group?
    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        ordering = ['name']


class SpecialPrices(models.Model):
    # customer = models.ForeignKey('employees.Customer', blank=False, null=False, related_name='taskin_customer')
    product = models.ForeignKey('products.Product', related_name="special_prices_items", null=False, blank=False)
    price = models.FloatField(verbose_name=_('Price'), blank=False, null=False)
    group = models.ForeignKey('CustomerGroup', blank=False, null=False, related_name='taskin_special_price_group')
    archived = models.BooleanField(default=False)

    def __unicode__(self):
        return u'Special price for <%s> = $%s' % (self.product.name, self.price)

    class Meta:
        ordering = ['price']
