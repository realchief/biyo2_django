from datetime import datetime

import pytz
import logging
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from localflavor.us.us_states import STATE_CHOICES
from simple_history.models import HistoricalRecords
from .utils import resize_image

logger = logging.getLogger(__name__)

PRODUCT_IMAGE_SIZE = (200, 200)

COLORS = (
    (1, 'Orange'),
    (2, 'Aqua'),
    (3, 'Brown'),
    (4, 'Green'),
    (5, 'Cyan'),
    (6, 'Purple'),
    (7, 'Pink')
)

IMAGES = (
    (1, 'Square'),
    (2, 'Circle'),
    (3, 'Rectangle')
)

DISCOUNT_TYPES = (
    (1, "Percentage Off"),
    (2, "Dollars Off"),
)


class Category(models.Model):
    parent = models.ForeignKey('Category', blank=True, null=True)
    name = models.CharField(verbose_name=_('Name'), max_length=64)
    color = models.IntegerField(choices=COLORS, verbose_name=_('Color'))
    sorting = models.IntegerField(verbose_name=_('Sorting'), default=0, max_length=255)
    active = models.BooleanField(verbose_name=_('Active'), default=True)
    # image = models.ImageField(verbose_name=_('Image'), upload_to="category_images", blank=True, null=True)
    image = models.ImageField(upload_to='category_images/', verbose_name=_('Image'), blank=True, null=True)
    archived = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        ordering = ('sorting',)

    def save(self, *args, **kwargs):
        if self.pk and self.parent == self.pk:
            raise ValidationError("Category cannot be parent of itself!")
        return super(Category, self).save(*args, **kwargs)


class TaxRate(models.Model):
    rate = models.FloatField(verbose_name=_("Rate"))
    name = models.CharField(verbose_name=_("Tax Name"), max_length=64)
    archived = models.BooleanField(default=False)

    def __unicode__(self):
        return u'{0}: {1}%'.format(self.name, self.rate)

    class Meta:
        ordering = ['name']


class ModifierGroup(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=64)
    select_multiple = models.BooleanField(default=False, verbose_name=_('Select Multiple'))
    archived = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % self.name


class Modifier(models.Model):
    group = models.ManyToManyField(ModifierGroup, related_name='modifiers',
                                   verbose_name=_('Groups'))
    name = models.CharField(verbose_name=_('Name'), max_length=64)
    cost = models.FloatField(verbose_name=_('Cost'))
    price = models.FloatField(verbose_name=_('Price'))
    active = models.BooleanField(verbose_name=_('Active'), default=True)
    archived = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % self.name


class Printer(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=64)
    local_ip = models.CharField(max_length=128, null=True, blank=True)
    archived = models.BooleanField(default=False)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % self.name


class Product(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=64)
    description = models.CharField(verbose_name='Description', max_length=224, blank=True, null=True)
    image = models.ImageField(upload_to='product_images/', verbose_name=_('Image'), blank=True, null=True)
    color = models.IntegerField(choices=COLORS, verbose_name=_('Color'), blank=True, null=True, max_length=255)
    sorting = models.IntegerField(verbose_name=_('Sorting'), default=0, blank=True, null=True, max_length=255)
    cost = models.FloatField(verbose_name=_('Cost'), blank=True, null=True, default=0.0, max_length=255)
    price = models.FloatField(verbose_name=_('Price'), blank=True, null=True, default=0.0, max_length=255)
    barcode = models.CharField(verbose_name=_('Barcode'), blank=True, null=True, max_length=255)
    stock = models.IntegerField(verbose_name=_('Stock'), blank=True, null=True, default=0, max_length=255)
    categories = models.ManyToManyField(Category, related_name="products", blank=True, null=True)
    suppliers = models.ManyToManyField('employees.Supplier', related_name="suppliers", blank=True, null=True)
    modifier_groups = models.ManyToManyField(ModifierGroup, related_name="products", blank=True, null=True)
    tax_rate = models.ForeignKey(TaxRate, related_name="taxrate", verbose_name=_('Tax Rate'), blank=True, null=True)
    # tax_status = models.IntegerField(verbose_name=_('Tax status'), choices=((0, "Taxed"), (1, "Not taxed")), default=0, max_length=255)
    active = models.BooleanField(verbose_name=_('Active'), default=True)
    # price_adjust = models.FloatField(blank=True, null=True)
    archived = models.BooleanField(default=False)
    price_adjust = models.BooleanField(verbose_name=_('Ask price everytime?'), choices=((True, "Yes"), (False, "No")),
                                       default=False)

    # print_to = models.BooleanField(verbose_name=_('Print to Kitchen'), default=False,
    #                                choices=((True, "Yes"), (False, "No")))

    printer = models.ForeignKey(Printer, related_name="printer", verbose_name=_('Which Printer'), blank=True, null=True)

    change_reason = models.CharField(max_length=100, null=True, default='', blank=True)
    stock_change = models.IntegerField(default=0, max_length=255)
    history = HistoricalRecords()

    class Meta:
        ordering = ('sorting',)

    def __unicode__(self):
        return u'%s' % self.name

    def get_categories(self):
        if hasattr(self, 'category_prods'):
            return [int(c.id) for c in self.category_prods]
        if not hasattr(self, '_categories'):
            self._categories = list(self.categories.all().values('id', 'name'))
        cats = list(int(c['id']) for c in self._categories)
        return cats

    def get_cat_names(self):
        if hasattr(self, 'category_prods'):
            return ','.join(c.name for c in self.category_prods)
        if not hasattr(self, '_categories'):
            self._categories = list(self.categories.all().values('id', 'name'))
        cats = list(c['name'] for c in self._categories)
        return ",".join(cats)

    def save(self, *args, **kwargs):
        try:
            recent_product = self.history.most_recent()
            if recent_product:
                self.stock_change = (self.stock or 0) - (recent_product.stock or 0)
        except self.history.instance.DoesNotExist:
            pass
        if self.image:
            try:
                self.image = resize_image(self.image, newsize=PRODUCT_IMAGE_SIZE)
            except:
                logger.exception("Error resizing image for product %s" % self.pk)
        return super(Product, self).save(*args, **kwargs)


class Discount(models.Model):
    name = models.CharField(max_length=128, verbose_name=_('Name'))
    value = models.FloatField(verbose_name=_('Value'))
    type = models.IntegerField(choices=DISCOUNT_TYPES, verbose_name=_('Type'))
    archived = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return u'%s' % self.name


INDUSTRY_CHOICES = (
    ("RETAIL", "RETAIL"),
    ("MOTO", "MOTO"),
    ("RESTAURANT", "RESTAURANT"),
    ("ECOMMERCE", "ECOMMERCE"),
)


class Store(models.Model):
    archived = models.BooleanField(default=False)
    name = models.CharField(max_length=128, verbose_name=_('Name'))
    logo = models.ImageField(upload_to="store_images", null=True, blank=True, verbose_name=_('Logo'))
    number = models.IntegerField(verbose_name=_('Number'))
    address = models.CharField(max_length=128, verbose_name=_('Address'))
    address_2 = models.CharField(max_length=128, null=True, blank=True, verbose_name=_('Second Address'))
    city = models.CharField(max_length=128, verbose_name=_('City'))
    state = models.CharField(verbose_name=_('State'), max_length=100, choices=STATE_CHOICES)
    zipcode = models.CharField(verbose_name=_('Zipcode'), max_length=128)
    phone = models.CharField(verbose_name=_('Phone'), max_length=16, null=True, blank=True)
    fax = models.CharField(max_length=16, verbose_name=_('Fax'), null=True, blank=True)
    email = models.CharField(max_length=128, verbose_name=_('Email'), null=True, blank=True)
    website = models.URLField(verbose_name=_('Website'), null=True, blank=True)
    tax_rate = models.ForeignKey(TaxRate, related_name="stores", verbose_name=_('Tax Rate'), null=True, blank=True)
    package = models.IntegerField(verbose_name=_('Package'))
    timezone = models.CharField(max_length=64, choices=[(x, x) for x in pytz.common_timezones])
    xweb_url = models.CharField(max_length=128, verbose_name=_('XWeb URL'))
    xweb_id = models.CharField(max_length=128, verbose_name=_('XWeb ID'))
    xweb_terminal_id = models.CharField(max_length=128, verbose_name=_('XWeb Terminal ID'))
    xweb_auth_key = models.CharField(max_length=128, verbose_name=_('XWeb Auth Key'))
    xweb_industry = models.CharField(max_length=128, verbose_name=_('XWeb Industry'), choices=INDUSTRY_CHOICES)

    def __unicode__(self):
        return u'%s' % self.name


class TableSection(models.Model):
    archived = models.BooleanField(default=False)
    store = models.ForeignKey(Store, related_name="sections", verbose_name=_('Store'))
    section_name = models.CharField(max_length=128, verbose_name=_('Section Name'))

    def __unicode__(self):
        return u'%s' % self.section_name

    def get_tables(self):
        return self.tables.filter(archived=False)


class Table(models.Model):
    archived = models.BooleanField(default=False)
    section = models.ForeignKey(TableSection, related_name="tables", verbose_name=_('Section'))
    table_name = models.CharField(max_length=128, verbose_name=_('Table Name'))
    table_image = models.IntegerField(max_length=1, choices=IMAGES, blank=True, null=True,
                                      verbose_name=_('Table Image'))
    x_value = models.FloatField(null=True, blank=True, verbose_name=_('X Value'))
    y_value = models.FloatField(null=True, blank=True, verbose_name=_('Y Value'))
    number_people = models.IntegerField(verbose_name=_('Number of People'))
    current_order = models.ForeignKey('order.Order', related_name="tables", null=True, blank=True,
                                      verbose_name=_('Current Order'))

    def __unicode__(self):
        return u'%s' % self.table_name


TERMINAL_MODES = (
    (1, 'Table Service'),
    (2, 'Quick Service')
)

REWARD_CHOISES = (
    (1, 'Percentage'),
    (2, 'Dollars off')
)


class Terminal(models.Model):
    name = models.CharField(max_length=128)
    mac_id = models.CharField(max_length=128)
    pole_display = models.CharField(max_length=128, null=True, blank=True)
    mode = models.IntegerField(null=True, blank=True, choices=TERMINAL_MODES)
    local_ip = models.CharField(max_length=128, null=True, blank=True)
    receipt_printer = models.CharField(max_length=128, null=True, blank=True)
    station_number = models.IntegerField(null=True, blank=True)
    master = models.IntegerField(null=True, blank=True)
    archived = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % self.name

    def get_name(self):
        return self.name


class Reward(models.Model):
    name = models.CharField(max_length=250, verbose_name=_('Name of Reward'))
    store = models.ForeignKey(Store, verbose_name=_('Store'))
    points_redeem = models.IntegerField(verbose_name=_('Amount of Points to Redeem'), null=True)
    discount = models.CharField(max_length=250, verbose_name=_('Reward Type'),
                                choices=(("Discount", "Discount"), ("Text", "Text")))
    discount_type = models.CharField(max_length=250, verbose_name=_('Discount Type'),
                                     choices=(("Item", "Item"), ("Invoice", "Invoice")))
    discount_type_item = models.ForeignKey(Product, verbose_name=_('Discount Item'), related_name='product_item',
                                           null=True, blank=True)
    # discount_type_invoice =>discount_value
    discount_value = models.CharField(max_length=128, verbose_name=_('Discount Value'), null=True, blank=True)
    discount_text = models.CharField(max_length=250, verbose_name=_('Discount Text'), null=True, blank=True)
    reward_type = models.IntegerField(verbose_name=_('Percentage or Dollars off'), choices=REWARD_CHOISES, default=2)
    archived = models.BooleanField(default=False, verbose_name=_('Disable Reward'))
    active = models.BooleanField(default=True, verbose_name=_('Active'), choices=((True, "True"), (False, "False")))

    def __unicode__(self):
        return u'%s' % self.name


class Csv(models.Model):
    group_csv = models.FileField(upload_to='csv', blank=False, null=False)
    created = models.DateTimeField(editable=False)

    def __unicode__(self):
        return u'%s' % self.group_csv

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = datetime.today()
        return super(Csv, self).save(*args, **kwargs)
