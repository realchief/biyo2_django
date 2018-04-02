from datetime import datetime, timedelta
import logging

from django.contrib.auth import hashers
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, models, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from localflavor.us.us_states import STATE_CHOICES

from employees.utils import generate_random_emails
from products.models import Store
from products.utils import resize_image
from taskin.models import CustomerGroup

from django_countries.fields import CountryField
logger = logging.getLogger(__name__)

ROLES = (
    (1, 'Owner'),
    (2, 'Manager'),
    (3, 'Cashier'),
    (4, 'Employee'),
)

EMPLOYEE_PHOTO_SIZE = (128, 128)

class EmployeeManager(BaseUserManager):
    def create_user(self, email, password, name, role, address=None, city=None,
                    state=None, zipcode=None, phone=None, pin=None,
                    hourly_rate=None, address2=None, store=None, photo=None):
        # XXX: Using dummy user
        # if not email:
        #     email = generate_random_emails(10)
        # if not password:
        #     from random import randrange
        #     password = randrange(1000)

        email = EmployeeManager.normalize_email(email)
        employee = Employee()
        employee.email = email
        employee.password = hashers.make_password(password, phone)
        employee.name = name
        employee.address = address
        employee.address2 = address2
        employee.city = city
        employee.state = state
        employee.zipcode = zipcode
        employee.phone = phone
        employee.hourly_rate = hourly_rate
        employee.pin = pin
        employee.role = role
        employee.is_active = True
        employee.store = store
        employee.photo = photo
        employee.save()
        return employee

    def create_superuser(self, email, password):
        # XXX: Didn't work
        name = 'default'
        employee = self.create_user(email, password, name, role=1)
        employee.is_staff = employee.is_active = employee.is_superuser = True
        employee.save()
        return employee


class Employee(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name=_('Email'), null=False, blank=False)
    photo = models.ImageField(upload_to='employee_photo/', verbose_name=_('P'), blank=True, default='employee_photo/def.jpg')
    name = models.CharField(verbose_name=_('Name'), max_length=32)
    address = models.CharField(verbose_name=_('Address'), max_length=32, null=True, blank=True)
    address2 = models.CharField(verbose_name=_("Address2"), null=True, blank=True, max_length=32)
    city = models.CharField(verbose_name=_('City'), max_length=32, null=True, blank=True)
    state = models.CharField(verbose_name=_('State'), max_length=2, choices=STATE_CHOICES, null=True, blank=True)
    zipcode = models.CharField(verbose_name=_('Zip code'), max_length=8, null=True, blank=True)
    phone = models.CharField(verbose_name=_('Phone'), max_length=60, null=True, blank=True)
    pin = models.IntegerField(verbose_name=_('Pin'), unique=True, null=True)
    role = models.IntegerField(verbose_name=_('Role'), choices=ROLES)
    vein_string = models.TextField(blank=True, verbose_name=_('Vein String'))
    hourly_rate = models.DecimalField(blank=True, null=True, verbose_name=_('Hourly Rate'), decimal_places=2,
                                      max_digits=5)
    archived = models.BooleanField(default=False)
    store = models.ForeignKey(Store, verbose_name='Store', blank=True, null=True)

    USERNAME_FIELD = 'email'

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(editable=False)

    objects = EmployeeManager()

    def __unicode__(self):
        return u"%s" % self.name

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def check_is_owner(self):
        return self.role == ROLES[0][0]

    def return_id(self):
        return self.id

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if self.photo:
            try:
                self.photo = resize_image(self.photo, newsize=EMPLOYEE_PHOTO_SIZE)
            except:
                logger.exception("Error resizing image for product %s" % self.pk)
                pass
        if not self.id:
            self.created = datetime.today()
        return super(Employee, self).save(*args, **kwargs)


class Customer(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)
    profile_key = models.CharField(max_length=32, null=True, blank=True)
    address = models.CharField(max_length=32, null=True, blank=True)
    rewards_points = models.IntegerField(null=True, blank=True)
    account_number = models.CharField(max_length=64, blank=True)
    notes = models.TextField(null=True, blank=True)
    archived = models.BooleanField(default=False)
    created = models.DateTimeField(editable=False)
    city = models.CharField(verbose_name=_('City'), max_length=58, null=True, blank=True)
    state = models.CharField(verbose_name=_('State'), max_length=2, choices=STATE_CHOICES, null=True, blank=True)
    zipcode = models.CharField(verbose_name=_('Zip code'), max_length=8, null=True, blank=True)
    group = models.ForeignKey(CustomerGroup, blank=True, null=True, related_name='taskin_group')

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)

    def save(self, *args, **kwargs):
        """
        On save, update timestamps
        """
        if not self.id:
            self.created = datetime.today()
        return super(Customer, self).save(*args, **kwargs)

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name


class TimeClock(models.Model):
    employee = models.ForeignKey(Employee, related_name='time_clock')
    time_in = models.DateTimeField()
    time_out = models.DateTimeField(null=True)
    archived = models.BooleanField(default=False)

    def time_range(self):
        try:
            return self.time_out - self.time_in
        except:
            pass
        return timedelta(seconds=0)

    def __unicode__(self):
        return u'Time entry for %s' % self.employee.name


class CsvCustomer(models.Model):
    group_csv = models.FileField(upload_to='csv', blank=False, null=False)
    created = models.DateTimeField(editable=False)

    def __unicode__(self):
        return u'%s' % self.group_csv

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = datetime.today()
        return super(CsvCustomer, self).save(*args, **kwargs)


class Supplier(models.Model):
    supplier = models.CharField(verbose_name=_('Supplier Name'), max_length=32)
    default_markup = models.PositiveIntegerField(verbose_name=_('Default Markup'), default=0, max_length=255)
    description = models.TextField(blank=True, verbose_name=_('Description'))
    company = models.CharField(verbose_name=_('Company'), max_length=32)
    first_name = models.CharField(verbose_name=_('First Name'), max_length=32)
    last_name = models.CharField(verbose_name=_('Last Name'), max_length=32)
    archived = models.BooleanField(default=False)
    created = models.DateTimeField(editable=False)
    phone = models.CharField(verbose_name=_('Phone'), max_length=60, null=True, blank=True)
    mobile = models.CharField(verbose_name=_('Mobile Phone'), max_length=60, null=True, blank=True)
    fax = models.CharField(verbose_name=_('Fax'), max_length=60, null=True, blank=True)
    email = models.EmailField(unique=True, verbose_name=_('Email'), null=False, blank=False)
    website = models.URLField(verbose_name=_('Website'), null=True, blank=True)
    street = models.CharField(verbose_name=_('Street'), max_length=32, null=True, blank=True)
    suburb = models.CharField(verbose_name=_('Suburb'), max_length=32, null=True, blank=True)
    city = models.CharField(verbose_name=_('City'), max_length=32, null=True, blank=True)
    postcode = models.CharField(verbose_name=_('Post Code'), max_length=8, null=True, blank=True)
    state = models.CharField(verbose_name=_('State'), max_length=2, choices=STATE_CHOICES, null=True, blank=True)
    country = CountryField(blank_label='(select a country)')

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)

    def save(self, *args, **kwargs):
        """
        On save, update timestamps
        """
        if not self.id:
            self.created = datetime.today()
        return super(Supplier, self).save(*args, **kwargs)
