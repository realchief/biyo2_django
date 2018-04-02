from __future__ import absolute_import
from django.db import models

from employees.models import Employee

TRANSACTION_TYPE_CHOICES = (
    (1, 'Sale'),
    (2, 'Void'),
    (3, 'Return'),
)


class Shift(models.Model):
    """
    ORM is supposed to control cash flow of the cash drawer during that shift.
    """
    terminal = models.ForeignKey('products.Terminal', related_name="shift_terminal", blank=False)
    open_shift_employee = models.ForeignKey(Employee, related_name="employee_opened", blank=False)
    close_shift_employee = models.ForeignKey(Employee, related_name="employee_closed", blank=True, null=True)
    shift_open_date = models.DateTimeField(auto_now_add=True)
    shift_update_date = models.DateTimeField(auto_now=True)
    shift_close_date = models.DateTimeField(blank=True, null=True)
    opening_amount = models.FloatField(blank=True, null=True, default=.0)
    total_cashtenders = models.FloatField(blank=True, null=True, default=.0)
    total_cashreturns = models.FloatField(blank=True, null=True, default=.0)
    total_drops = models.FloatField(blank=True, null=True, default=.0)
    total_payouts = models.FloatField(blank=True, null=True, default=.0)
    closing_amount = models.FloatField(blank=True, null=True, default=.0)
    over_shortage = models.FloatField(blank=True, null=True, default=.0)

    def __unicode__(self):
        return u"{0}'s shift at {1}".format(self.open_shift_employee.name, self.shift_open_date.strftime("%d-%m-%y"))


class Payout(models.Model):
    """
    ORM is supposed to describe payout bound with employee, terminal and processing shift.
    """
    employee = models.ForeignKey(Employee)
    shift = models.ForeignKey(Shift, blank=True, null=True, related_name='shift_payouts')
    terminal = models.ForeignKey('products.Terminal')
    payout_type = models.CharField(max_length=7, choices=[("IN", "IN"), ("OUT", "OUT"), ("DEPOSIT", "DEPOSIT")])
    payout_value = models.FloatField(blank=True, null=True, default=.0)
    payout_time = models.DateTimeField(blank=True, null=True)
    payout_note = models.CharField(max_length=100, blank=True, null=True, default="")


class Payment(models.Model):
    order = models.ForeignKey('order.Order', related_name="payments")
    employee = models.ForeignKey(Employee, related_name='payments_accepted', null=True, blank=True)
    amount = models.FloatField()
    amount_paid = models.FloatField(null=True)
    tips = models.FloatField(null=True, blank=True)
    change_amount = models.FloatField()
    card_lastfour = models.CharField(max_length=4, null=True, blank=True)
    payment_type = models.CharField(max_length=255)
    payment_date = models.DateTimeField()
    payment_form = models.CharField(max_length=64, null=True, blank=True)
    authorization = models.CharField(max_length=64, null=True, blank=True)
    transaction_type = models.IntegerField(choices=TRANSACTION_TYPE_CHOICES)
    processor_response = models.CharField(max_length=100)
    batch_num = models.CharField(max_length=100, null=True, blank=True)
    approval_code = models.IntegerField(null=True, blank=True)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    terminal_id = models.IntegerField(null=True, blank=True)
    signature = models.TextField(null=True, blank=True)
    void_ref = models.IntegerField(null=True, blank=True)
    shift = models.ForeignKey(Shift, blank=True, null=True)
    check_number = models.CharField(max_length=20, null=True, blank=True)
