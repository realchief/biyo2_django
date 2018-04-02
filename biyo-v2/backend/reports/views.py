# -*- coding: utf-8 -*-
import datetime
import json
import os
import time
from collections import Counter
from decimal import Decimal
from operator import itemgetter

import pytz
from django import http
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.humanize.templatetags.humanize import intcomma
from django.core import serializers
from django.core.urlresolvers import reverse
from django.db.models import Q, Count, Sum, F
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import floatformat
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.views import generic as cbv

from employees.models import Employee, Customer
from forms import EmployeeFilterForm
from order.models import Order, OrderItem
from panel import decorators
from payments import models as payment_models
from payments.models import Payment, Shift
from products import models as product_models

# from panel.decorators import decorators
from products.models import Product, Terminal
from reports.forms import CustomerPaymentForm, ReportsSortForm
from reports.utils import JSONResponseMixin
from settings.routers import get_default_db_connection

CUR_DIR = os.path.dirname(__file__)


class PDFResponseMixin(object):
    pdf_name = 'pdf'

    def link_callback(self, uri, rel):
        # use short variable names
        sUrl = settings.STATIC_URL
        sRoot = settings.STATIC_ROOT
        mUrl = settings.MEDIA_URL
        mRoot = settings.MEDIA_ROOT

        # convert URIs to absolute system paths
        path = ''
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))

            # make sure that file exists
            if not os.path.isfile(path):
                raise Exception(
                    'media URI must start with %s or %s' % (sUrl, mUrl)
                )
        # print("path: %s" % path)
        return os.path.abspath(path)

    def render_to_response(self, context):
        from xhtml2pdf import pisa
        from sx.pisa3 import pisaDocument
        import cStringIO as StringIO

        html = render_to_string(self.get_template_names(), context)
        result = StringIO.StringIO()
        # pdf = pisaDocument(StringIO.StringIO(html.encode("utf-8")), result, link_callback=self.link_callback)
        # result = result.getvalue()
        file_path = os.path.join(
            settings.MEDIA_ROOT,
            '%s_%s.pdf' % (self.pdf_name, datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S"))
        )
        file_path = os.path.abspath(file_path)
        pdffile = open(file_path, 'w+b')
        # pdffile.write(result)
        pisa_status = pisa.CreatePDF(html, dest=pdffile, link_callback=self.link_callback)

        pdffile.seek(0)
        pdf = pdffile.read()
        pdffile.close()

        resp = http.HttpResponse(
            pdf,
            content_type='application/pdf'
        )
        os.remove(file_path)
        return resp


@decorators.dispatch_decorator(login_required)
class BaseProductForReportsView(cbv.ListView, JSONResponseMixin):
    model = product_models.Product

    def render_to_response(self, context):
        # Look for a 'format=json' GET argument
        if self.request.GET.get('format') == 'json':
            return self.render_to_json_response(context)
        else:
            store = product_models.Store.objects.get(pk=1)
            context['tz'] = store.timezone
            context['store'] = store

            context['saved_url'] = self.get_saved_time_period(self, store)

            if self.request.GET.get('start') and self.request.GET.get('end'):
                context['current_date'] = '?start=' + str(self.request.GET['start']) + '&end=' + str(
                    self.request.GET['end'])
            else:
                context['current_date'] = ''
            return super(BaseProductForReportsView, self).render_to_response(context)

    def get_queryset(self):
        qs = super(BaseProductForReportsView, self).get_queryset()
        qs.prefetch_related('items')

        sorted_qs = sorted(qs, key=lambda product: len(product.order_items.all()), reverse=True)
        return sorted_qs

    @staticmethod
    def get_start_end_dates(request, week=False):
        start = request.GET.get('start')
        end = request.GET.get('end')
        if start and end:
            start, end = time.strptime(start, '%B%d,%Y%I:%M%p'), time.strptime(end, '%B%d,%Y%I:%M%p')
            start, end = datetime.datetime.fromtimestamp(time.mktime(start)),\
                         datetime.datetime.fromtimestamp(time.mktime(end))

        else:
            if not week:
                # start = end = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
                start = datetime.date.today().strftime('%B%d,%Y12:00AM')
                end = datetime.date.today().strftime('%B%d,%Y11:59PM')

                start, end = time.strptime(start, '%B%d,%Y%I:%M%p'), time.strptime(end, '%B%d,%Y%I:%M%p')
                start, end = datetime.datetime.fromtimestamp(time.mktime(start)),\
                             datetime.datetime.fromtimestamp(time.mktime(end))

            else:
                today = datetime.date.today()
                weekday = today.weekday()
                start, end = weekday, 6 - weekday
                start, end = today - datetime.timedelta(days=start), today + datetime.timedelta(days=end)
        try:
            tz = product_models.Store.objects.first().timezone
            tz = pytz.timezone(tz)
            start, end = tz.localize(start), tz.localize(end)
        except:
            pass
        end += datetime.timedelta(seconds=59)
        return start, end

    @staticmethod
    def get_orders_with_range(start, end, full=False):
        if full:
            queryset = Order.objects.filter(
                Q(open_date__range=(start, end)) | Q(close_date__range=(start, end))).exclude(close_date__gt=end)
        else:
            queryset = Order.objects.filter(Q(open_date__range=(start, end)) | Q(close_date__range=(start, end)),
                                            status=3).exclude(close_date__gt=end)
        return queryset

    @staticmethod
    def get_orders_with_shift(shift_id):
        """
        Method returns QuerySet of orders of matched shift.
        :param shift_id: int ID of Shift object.
        :return: Query object.
        """
        return Order.objects.filter(shift_id=shift_id)

    @staticmethod
    def get_payments_with_shift(shift_id):
        """
        Method returns QuerySet of orders of matched shift.
        :param shift_id: int ID of Shift object.
        :return: Query object.
        """
        return Payment.objects.filter(shift_id=shift_id)

    @staticmethod
    def get_saved_time_period(self, store):
        start = self.request.GET.get('start', False)
        end = self.request.GET.get('end', False)
        current_url = '?start=' + str(start) + '&end=' + str(end) + '&option=0'
        if 'url' in self.request.session:
            saved_url = self.request.session['url']
            if current_url == saved_url:
                return saved_url
            elif not start and not end:
                return saved_url
            else:
                self.request.session['url'] = current_url
                return current_url
        else:
            if not isinstance(store, product_models.Store):
                store = product_models.Store.objects.get(pk=1)
            tz = store.timezone
            tz = pytz.timezone(tz)
            fmt_start = '%B%d,%Y12:00AM'
            fmt_end = '%B%d,%Y11:59PM'
            utc = pytz.utc
            utc_dt = utc.localize(datetime.datetime.now())
            local_dt = tz.normalize(utc_dt.astimezone(tz))
            start = local_dt.strftime(fmt_start)
            end = local_dt.strftime(fmt_end)
            current_url = '?start=' + str(start) + '&end=' + str(end) + '&option=0'
            self.request.session['url'] = current_url
        return current_url


@decorators.dispatch_decorator(login_required)
class PaymentView(BaseProductForReportsView):
    model = payment_models.Payment
    template_name = 'reports/payments.html'

    def get_queryset(self):
        pass

    def get_context_data(self):
        start, end = BaseProductForReportsView.get_start_end_dates(self.request)
        qs = self.model.objects.filter(
            Q(order__open_date__range=(start, end)) | Q(order__close_date__range=(start, end)),
            order__status=3).exclude(order__close_date__gt=end)
        total_card_sum = qs.exclude(payment_type='Cash').filter(order__status=3).aggregate(sum=Sum('amount'))['sum']
        cash = qs.filter(payment_type='Cash').values('amount', 'change_amount')
        other_cc = qs.filter(payment_type='OtherCredit').aggregate(sum=Sum('amount'))['sum']
        refunded = qs.filter(order__status=5).exclude(transaction_type=1).aggregate(sum=Sum('amount'))['sum']
        cash_sum = 0
        cash_sum_list = list(cash)
        for i in cash_sum_list:
            cash_sum += i['amount'] - i['change_amount']
        tips_sum = qs.aggregate(sum=Sum('tips'))['sum']

        if not isinstance(total_card_sum, float):
            total_card_sum = 0

        if not isinstance(cash_sum, float):
            cash_sum = 0

        if not isinstance(tips_sum, float):
            tips_sum = 0

        if not isinstance(other_cc, float):
            other_cc = 0

        total_before_tips = total_card_sum + cash_sum
        total_sum = total_before_tips + tips_sum
        return {
            'refunded': refunded,
            'total_card_sum': total_card_sum,
            'total_before_tips': total_before_tips,
            'tips_sum': tips_sum,
            'other_cc': other_cc,
            'total_sum': total_sum,
            'cash_sum': cash_sum,
            'visa_sum': qs.filter(
                payment_type='Visa'
            ).aggregate(sum=Sum('amount'))['sum'],
            'mastercard_sum': qs.filter(
                payment_type='MasterCard'
            ).aggregate(sum=Sum('amount'))['sum'],
            'american_express_sum': qs.filter(
                payment_type='American Express'
            ).aggregate(sum=Sum('amount'))['sum'],
            'discover_sum': qs.filter(
                payment_type='Discover'
            ).aggregate(sum=Sum('amount'))['sum'],
            'start_date': start.strftime('%B %d, %Y'),
            'end_date': end.strftime('%B %d, %Y'),
        }


class SalesSummaryView(BaseProductForReportsView):
    template_name = 'reports/sales_summary.html'
    model = Order

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        start, end = self.get_start_end_dates(self.request)
        qs = self.get_orders_with_range(start, end, True)
        payments = Payment.objects.filter(
            Q(order__open_date__range=(start, end)) | Q(order__close_date__range=(start, end)),
            order__status=3).exclude(order__close_date__gt=end)

        terminal = self.request.POST.get('terminal')
        if terminal:
            self.request.session['terminal'] = terminal
            qs = qs.filter(terminal_id=terminal)
            payments = payments.filter(terminal_id=terminal)
        elif terminal == '':
            if 'terminal' in self.request.session:
                del self.request.session['terminal']
        elif 'terminal' in self.request.session:
            qs = qs.filter(terminal_id=self.request.session['terminal'])
            payments = payments.filter(terminal_id=self.request.session['terminal'])

        employee = self.request.POST.get('employees')
        if employee:
            self.request.session['employee'] = employee
            qs = qs.filter(emp_close_id=employee)
            payments = payments.filter(employee_id=employee)
        elif employee == '':
            if 'employee' in self.request.session:
                del self.request.session['employee']
        elif 'employee' in self.request.session:
            qs = qs.filter(emp_close_id=self.request.session['employee'])
            payments = payments.filter(employee_id=self.request.session['employee'])

        form = ReportsSortForm(self.request)
        total_card_sum = payments.exclude(payment_type='Cash').exclude(payment_type='Check').aggregate(sum=Sum('amount'))['sum']
        check = payments.filter(payment_type='Check').values('amount', 'change_amount')
        cash = payments.filter(payment_type='Cash').values('amount', 'change_amount')
        account = payments.filter(payment_type='Account').values('amount', 'change_amount')
        other_cc = payments.filter(payment_type='OtherCredit').aggregate(sum=Sum('amount'))['sum']
        refunded = qs.filter(status=5).aggregate(sum=Sum('grand_total'))['sum']
        check_sum = 0
        cash_sum = 0
        cash_sum_list = list(cash)
        for i in cash_sum_list:
            cash_sum += i['amount'] - i['change_amount']
        check_sum_list = list(check)
        for i in check_sum_list:
            check_sum += i['amount'] - i['change_amount']
        tips_sum = payments.aggregate(sum=Sum('tips'))['sum']

        account_sum = 0
        account_sum_list = list(account)
        for i in account_sum_list:
            account_sum += i['amount'] - i['change_amount']

        if not isinstance(total_card_sum, float):
            total_card_sum = 0

        if not isinstance(cash_sum, float):
            cash_sum = 0

        if not isinstance(check_sum, float):
            check_sum = 0

        if not isinstance(account_sum, float):
            account_sum = 0

        if not isinstance(tips_sum, float):
            tips_sum = 0

        if not isinstance(other_cc, float):
            other_cc = 0

        total_before_tips = total_card_sum + cash_sum + check_sum
        total_sum = total_before_tips + tips_sum

        transactions = qs.filter(open_date__gte=start, status=3)
        if transactions.count() != 0:
            average = float(total_sum)/float(transactions.count())
        else:
            average = float(0)
        open_orders = qs.filter(open_date__gte=start, status=1)
        close_orders = qs.filter(open_date__gte=start, status=3)
        hold_orders = qs.filter(open_date__gte=start, status=2)
        canceled_orders = qs.filter(open_date__gte=start, status=4)
        refunded_orders = qs.filter(open_date__gte=start, status=5)

        return {
            'store': product_models.Store.objects.first(),
            'discount': 0,
            'gross_sales': qs.filter(status=3).aggregate(sum=Sum('subtotal'))['sum'],
            'discount_total': qs.filter(status=3).aggregate(sum=Sum('discount_total'))['sum'],
            'grand_total': qs.filter(status=3).aggregate(sum=Sum('grand_total'))['sum'],
            'tax_total': qs.filter(status=3).aggregate(sum=Sum('tax_total'))['sum'],
            'tips': qs.filter(status=3).aggregate(sum=Sum('payments__tips'))['sum'],
            'active2': 'sales_summary',
            'form': form,
            'refunded': refunded,
            'total_card_sum': total_card_sum,
            'total_before_tips': total_before_tips,
            'tips_sum': tips_sum,
            'other_cc': other_cc,
            'total_sum': total_sum,
            'check_sum': check_sum,
            'cash_sum': cash_sum,
            'account_sum': account_sum,
            'visa_sum':
                payments.filter(Q(payment_type='Visa') | Q(payment_type='Visa Fleet')).aggregate(sum=Sum('amount'))[
                    'sum'],
            'mastercard_sum': payments.filter(payment_type='MasterCard').aggregate(sum=Sum('amount'))['sum'],
            'american_express_sum': payments.filter(payment_type='American Express').aggregate(sum=Sum('amount'))[
                'sum'],
            'discover_sum': payments.filter(payment_type='Discover').aggregate(sum=Sum('amount'))['sum'],

            'transactions': transactions.count(),
            'aver': average,
            'open_orders': open_orders.count(),
            'close_orders': close_orders.count(),
            'hold_orders': hold_orders.count(),
            'canceled_orders': canceled_orders.count(),
            'refunded_orders': refunded_orders.count(),
            'start_date': start.strftime('%B %d, %Y'),
            'end_date': end.strftime('%B %d, %Y'),
        }

    def post(self, request, *args, **kwargs):
       self.object_list = self.get_queryset()
       context = self.get_context_data()
       return self.render_to_response(context)


class SalesSummaryPDFView(PDFResponseMixin, SalesSummaryView):
    pdf_name = 'sales_summary'
    template_name = 'reports/pdf/sales_summary.html'


class EmployeeSalesSummaryView(BaseProductForReportsView):
    template_name = 'reports/employee_sales_summary.html'

    def get_context_data(self, **kwargs):
        context = super(EmployeeSalesSummaryView, self).get_context_data()
        return context

    def get_queryset(self):
        pass

    def get(self, request):
        form = EmployeeFilterForm(self.request.GET)
        saved_url = self.get_saved_time_period(self, False)
        return render(request, self.template_name, {'form': form, 'saved_url': saved_url})

    def post(self, request):
        form = EmployeeFilterForm(self.request.POST)
        if form.is_valid():
            start, end = self.get_start_end_dates(self.request)
            employee = Employee.objects.get(pk=form.cleaned_data['employees'].return_id())
            qs = employee.order_as_close.filter(Q(open_date__range=(start, end)) | Q(close_date__range=(start, end)),
                                                status=3).exclude(close_date__gt=end)
            payments = employee.payments_accepted.filter(
                Q(order__open_date__range=(start, end)) | Q(order__close_date__range=(start, end)),
                order__status=3).exclude(order__close_date__gt=end)
            total_card_sum = payments.exclude(payment_type='Cash').aggregate(sum=Sum('amount'))['sum']
            cash = payments.filter(payment_type='Cash').values('amount', 'change_amount')
            other_cc = payments.filter(payment_type='OtherCredit').aggregate(sum=Sum('amount'))['sum']
            refunded = payments.filter(order__status=5).exclude(transaction_type=1).aggregate(sum=Sum('amount'))['sum']
            cash_sum = 0
            cash_sum_list = list(cash)
            for i in cash_sum_list:
                cash_sum += i['amount'] - i['change_amount']
            tips_sum = payments.aggregate(sum=Sum('tips'))['sum']

            if not isinstance(total_card_sum, float):
                total_card_sum = 0

            if not isinstance(cash_sum, float):
                cash_sum = 0

            if not isinstance(tips_sum, float):
                tips_sum = 0

            if not isinstance(other_cc, float):
                other_cc = 0

            total_before_tips = total_card_sum + cash_sum
            total_sum = total_before_tips + tips_sum

            return render(self.request, self.template_name, {
                'refunded': refunded,
                'total_card_sum': total_card_sum,
                'total_before_tips': total_before_tips,
                'tips_sum': tips_sum,
                'other_cc': other_cc,
                'total_sum': total_sum,
                'cash_sum': cash_sum,
                'visa_sum':
                    payments.filter(Q(payment_type='Visa') | Q(payment_type='Visa Fleet')).aggregate(sum=Sum('amount'))[
                        'sum'],
                'mastercard_sum': payments.filter(payment_type='MasterCard').aggregate(sum=Sum('amount'))['sum'],
                'american_express_sum': payments.filter(payment_type='American Express').aggregate(sum=Sum('amount'))[
                    'sum'],
                'discover_sum': payments.filter(payment_type='Discover').aggregate(sum=Sum('amount'))['sum'],
                'gross_sales': qs.aggregate(sum=Sum('subtotal'))['sum'],
                'discount_total': qs.aggregate(sum=Sum('discount_total'))['sum'],
                'grand_total': qs.aggregate(sum=Sum('grand_total'))['sum'],
                'tax_total': qs.aggregate(sum=Sum('tax_total'))['sum'],
                'tips': qs.aggregate(sum=Sum('payments__tips'))['sum'],
                'form': form,
                'saved_url': self.get_saved_time_period(self, False),
                'start_date': start.strftime('%B %d, %Y'),
                'end_date': end.strftime('%B %d, %Y'),
            })
        else:
            return render(self.request, self.template_name, {'form': form})


class ItemSalesView(BaseProductForReportsView):
    template_name = 'reports/item_sales.html'

    def convert_context_to_json(self, context):
        products = context['products']
        outputlist = list()
        for product in products:
            try:
                name = product[0].name
            except AttributeError:
                name = product[0]
            if name != 'Custom Item':
                outputlist.append(
                    {"name": name, 'y': product[1]['item_sold'], 'x': round(product[1]['gross_sales'], 2)})

        return json.dumps(outputlist)

    def get_queryset(self):
        start, end = self.get_start_end_dates(self.request)
        orders = self.get_orders_with_range(start, end)
        items = OrderItem.objects.filter(order__in=orders).exclude(void_status=1)
        qs = items.values('product__name', 'product_id', 'product__barcode'). \
            annotate(
            total=Sum('price',
                      field='order_orderitem.quantity * (order_orderitem.price - order_orderitem.discount)'),
            amount=Sum('quantity'),
            discount=Sum('discount',
                         field='order_orderitem.quantity * order_orderitem.discount'),
            sales=Sum('price',
                      field='order_orderitem.quantity * order_orderitem.price')). \
            order_by('-amount', '-sales', 'product__name')
        return qs

    def get_context_data(self, **kwargs):
        context = super(ItemSalesView, self).get_context_data(**kwargs)
        start, end = self.get_start_end_dates(self.request)
        orders = self.get_orders_with_range(start, end)
        orders_discount = orders.aggregate(discounts=Sum('discount_total'))['discounts'] or 0
        qs = self.get_queryset()
        totals = qs.aggregate(count=Sum('amount'), sold=Sum('sales'), discounts=Sum('discount'))
        context.update({
            'discount': totals['discounts'] or 0,
            'total_items': totals['count'] or 0,
            'total_gross_sales': totals['sold'] or 0,
            'total_sum': (totals['sold'] or 0) - (totals['discounts'] or 0),
            'total_after_item_and_order_discount': (totals['sold'] or 0) - (totals['discounts'] or 0) - orders_discount,
            'start_date': start.strftime('%B %d, %Y'),
            'end_date': end.strftime('%B %d, %Y'),
        })
        return context


class CheckOrdersAndPayments(BaseProductForReportsView):
    template_name = 'reports/checkordersandpayments.html'

    def get_context_data(self, **kwargs):
        start, end = BaseProductForReportsView.get_start_end_dates(self.request)
        orders = self.get_orders_with_range(start, end, True).filter(status__in=(1, 2, 4))
        ordersout = list()
        for order in orders:
            payment = order.payments
            if payment.count() > 0:
                ordersout.append(order)

        return {"order": ordersout}

    def get_queryset(self):
        pass


def feq(a, b):
    try:
        if abs(a - b) < 0.00000001:
            return 1
        else:
            return 0
    except(TypeError):
        raise TypeError('Wrong types')


class CheckOrders(BaseProductForReportsView):
    model = payment_models.Payment
    template_name = 'reports/checkorders.html'

    def get_queryset(self):
        pass

    def get_context_data(self, **kwargs):
        start, end = BaseProductForReportsView.get_start_end_dates(self.request)
        outitem = list()
        orderout = list()
        order_without_items = list()
        orders = self.get_orders_with_range(start, end)
        # dupes = Payment.objects.raw("SELECT order_id, payment_date, amount_paid "
        # "FROM payments_payment group by payment_date,amount_paid having count(*) >= 2 ")

        for order in orders:
            items = order.items.exclude(void_status=1)
            payment = order.payments
            if (items.count() and payment.count()) > 0:

                summ_amount_paid = payment.aggregate(sum=Sum('amount_paid'))['sum']
                itemsumm = int()
                item_price = 0
                for item in items:
                    # itemsumm +=(item.price)*item.quantity
                    item_price += item.price * item.quantity

                # if not feq(item_price, order.subtotal) or \
                #         not feq(item_price, summ_amount_paid) or \
                #         not feq(order.subtotal, summ_amount_paid):
                #     order.subtotal=item_price
                #     order.description=summ_amount_paid
                #     orderout.append(order)

                if not feq(item_price, order.subtotal) and not feq(summ_amount_paid, order.grand_total):
                    order.subtotal = item_price
                    order.description = summ_amount_paid
                    outitem.append(order)

            else:
                order_without_items.append(order)
        return {"outitem": outitem, "orderout": orderout, 'order_without_items': order_without_items}


class ItemSalesPDFView(PDFResponseMixin, ItemSalesView):
    pdf_name = 'item_sales'
    template_name = 'reports/pdf/item_sales.html'


class DiscountSummary(BaseProductForReportsView):
    model = Order
    template_name = 'reports/discount_summary.html'

    def get_queryset(self):
        pass

    def get_context_data(self, **kwargs):
        start, end = self.get_start_end_dates(self.request)
        qs = self.get_orders_with_range(start, end)
        return {
            "number_of_orders": len(qs),
            "discounts_total": len(filter(lambda order: order.discount_total > 0, qs)),
            "amounts_deducted": sum(order.discount_total for order in qs),
            'current_date': '?start=' + str(start) + '&end=' + str(end),
            'start_date': start.strftime('%B %d, %Y'),
            'end_date': end.strftime('%B %d, %Y'),
        }


class HourlySales(BaseProductForReportsView):
    model = Order
    template_name = 'reports/hourly_sales.html'

    def get_queryset(self):
        pass

    def get_context_data(self, **kwargs):
        """
        Return list of dates split by hours with amount of sold items
        [
            'date': '13 March',
            'total': '10',
            'hours': [
                {
                    'amount': 0,
                    'hour': '00:00'
                },
                {
                    'amount': 10,
                    'hour': '01:00'
                }
            ]
        ]
        """
        start, end = self.get_start_end_dates(self.request)
        if start is not None or end is not None:
            hours = 24

            qs = self.get_orders_with_range(start, end)
            sorted_qs = sorted(qs, key=lambda x: x.close_date)

            date_range_split = list()
            date_range = end - start

            for day in range(date_range.days + 1):
                date = start + datetime.timedelta(day)
                day_split_by_hours = list()

                for hour in range(hours):
                    time = date + datetime.timedelta(hours=hour)
                    next_hour = time + datetime.timedelta(hours=1)
                    orders = filter(lambda x: time <= x.close_date <= next_hour, sorted_qs)
                    amount = len(orders)
                    sales = sum(order.grand_total for order in orders)

                    if amount > 0:
                        day_split_by_hours.append({
                            'hour': time.strftime("%I:%M %p"),
                            'amount': amount,
                            'sales': sales
                        })
                total = sum(day.get('amount') for day in day_split_by_hours)
                total_sales = sum(day.get('sales') for day in day_split_by_hours)
                if total > 0:
                    date_range_split.append({
                        'date': date.strftime("%B, %d"),
                        'hours': day_split_by_hours,
                        'total': total,
                        'total_sales': total_sales
                    })

            return {
                'sorted_qs': date_range_split,
                'start_date': start.strftime('%B %d, %Y'),
                'end_date': end.strftime('%B %d, %Y'),
            }
        else:
            return {}


class TestReport(BaseProductForReportsView):
    model = Order
    template_name = 'reports/accountant_summary_test.html'

    def get_queryset(self):
        pass

    def get_context_data(self, **kwargs):
        """
        Return sales per category
        {
            'category': amount_of_sales,
            'category': amount_of_sales
        }
        """
        start, end = self.get_start_end_dates(self.request)
        if start or end is not None:

            category_list = []
            misc_items = 0
            discount = 0
            category_sales = {}
            count_test_items = 0
            out = {}
            total = 0
            orders = self.get_orders_with_range(start, end)
            for order in orders:
                for item in order.items.exclude(void_status=True).all():
                    sales = item.price * item.quantity
                    # tax_total+=item.price*item.tax*item.quantity
                    count_test_items += item.quantity

                    product = item.product
                    # out['misc']={}
                    # if not product.categories.all():
                    # out['misc']={'categories':[]}
                    # else:
                    #     out['misc'] = {'sales':True, 'categories':product.categories.all()}
                    # print  out['misc']['categories']

                    for category in product.categories.all()[:1]:

                        if category.parent:
                            if category.parent in out:
                                if category in out[category.parent]['categories']:

                                    sale = out[category.parent]['categories'][category]
                                    sale[category] += sales
                                    out[category.parent]['categories'][category] = sale
                                    out[category.parent]['sales'] += sales
                                else:
                                    out[category.parent]['categories'][category] = {category: sales}
                                    out[category.parent]['sales'] += sales
                            else:
                                out[category.parent] = {'parent': True, 'categories': {}, 'sales': 0}
                                out[category.parent]['categories'][category] = {category: sales}
                                out[category.parent]['sales'] = sales

                        else:
                            if category in out:
                                # out[category]['categories'][category] = [category]
                                out[category]['sales'] += sales
                            else:
                                out[category] = {'parent': False, 'sales': 0}
                                out[category]['categories'] = [category]
                                out[category]['sales'] = sales

                    if not product.categories.all():
                        misc_items += item.quantity
                        if 'misc' in category_sales:
                            category_sales['misc'] += sales
                        else:
                            category_sales['misc'] = sales
                    else:
                        for category in product.categories.all()[:1]:
                            category_list += [category] * item.quantity
                            if category in category_sales:
                                category_sales[category] += sales
                            else:
                                category_sales[category] = sales

                discount += order.discount_total
            categories = Counter(category_list).items()
            new_categories = list()
            for category in categories:
                new_categories.append((category[0], category[1], category_sales[category[0]]))
            if misc_items != 0:
                new_categories.append(('Misc', misc_items, category_sales['misc']))
                total = misc_items
            total += sum(category[1] for category in categories)
            total_sales = sum(category[2] for category in new_categories)
            return {'output': out, 'discount': discount, 'categories': new_categories, 'total': total,
                    'total_sales': total_sales}
        else:
            return {}


class AccountantSummary(BaseProductForReportsView):
    model = Order
    template_name = 'reports/accountant_summary.html'

    def get_queryset(self):
        pass

    def convert_context_to_json(self, context):
        output = list()
        cats = context['categories']
        for category in cats:
            name = category['category']
            output.append({'name': name, 'itemcount': category['amount'], 'grand_total': category['sales']})
        return json.dumps(output)

    def get_context_data(self, **kwargs):
        """
        Return sales per category
        {
            'category': amount_of_sales,
            'category': amount_of_sales
        }
        """
        start, end = self.get_start_end_dates(self.request)
        if start or end is not None:
            orders = self.get_orders_with_range(start, end, False)
            """
                HERE we use RAW SQL queries. It is ease than construct huge queryset.
            """
            with open(os.path.join(CUR_DIR, 'sql', 'accountant_summary.sql.tpl'), 'r') as sqlfile:
                raw_sql = sqlfile.read()
            raw_sql = raw_sql.format(
                orderitem_tbl=OrderItem._meta.db_table,
                product2category_tbl=product_models.Product.categories.through._meta.db_table,
                order_tbl=Order._meta.db_table,
                open_date=pytz.utc.normalize(start).strftime('%Y-%m-%d %H:%M:%S'),
                close_date=pytz.utc.normalize(end).strftime('%Y-%m-%d %H:%M:%S'),
            )
            connection = get_default_db_connection(self.request)
            cursor = connection.cursor()
            cursor.execute(raw_sql)
            columns = [col[0] for col in cursor.description]
            category_data = {}
            total_discount = orders.aggregate(discounts=Sum('discount_total'))['discounts'] or 0
            total_quantity = 0
            total_sales = 0
            for row in cursor.fetchall():
                cdata = dict(zip(columns, row))
                category_data[cdata['category_id']] = cdata
                # total_discount += cdata['discount']
                total_quantity += cdata['amount']
                total_sales += cdata['sales']

            categories = dict(
                (c['id'], c)
                for c in product_models.Category.objects.all().values('id', 'name', 'parent', 'active', 'archived'))
            categories[None] = {'id': None, 'name': 'Uncategorized Items',
                                'parent': None, 'active': True, 'archived': False}
            for cid in categories:
                categories[cid].update({'sales': 0, 'amount': 0, 'percentage': 0, 'level': 0, 'child_cnt': 0})
            for cid in categories:
                if cid in category_data:
                    categories[cid]['sales'] = category_data[cid]['sales']
                    categories[cid]['amount'] = category_data[cid]['amount']
                if total_sales > 0:
                    categories[cid]['percentage'] = 100.0 * categories[cid]['sales'] / total_sales
                parent_id = categories[cid]['parent']
                prev_parent = None
                while parent_id:
                    if prev_parent is not None and prev_parent == parent_id:
                        # ERROR!! Category has itself as parent!
                        break
                    prev_parent = parent_id
                    categories[parent_id]['child_cnt'] += 1
                    parent_id = categories[parent_id]['parent']
                    categories[cid]['level'] += 1
            # sorting categories tree
            sorted_categories = []
            maxlevel = max(ctg['level'] for _, ctg in categories.items())
            for clevel in range(maxlevel + 1):
                thislevel_cats = [ctg for ctg in categories.values()
                                  if ctg['level'] == clevel and not
                    ((not ctg['active'] or ctg['archived']) and
                     ctg['child_cnt'] == 0 and ctg['amount'] == 0)]
                thislevel_cats = sorted(thislevel_cats, key=lambda x: (x['sales'], x['amount'], x['name']))
                if clevel == 0:
                    sorted_categories = list(reversed(thislevel_cats))
                    continue
                for subcat in thislevel_cats:
                    if (not subcat['active'] or subcat['archived']) and subcat['child_cnt'] == 0 \
                            and subcat['amount'] == 0:
                        # do not show last items if they are not active
                        continue
                    parent_pos = [pos for pos, c in enumerate(sorted_categories)
                                  if c['id'] == subcat['parent']] or [0]
                    sorted_categories.insert(parent_pos[0] + 1, subcat)

            results = {
                'discount': total_discount,
                'categories': sorted_categories,
                'total': total_quantity,
                'total_sales': total_sales,
                'start_date': start.strftime('%B %d, %Y'),
                'end_date': end.strftime('%B %d, %Y'),
            }
            return results
        else:
            return {}


class OrderGrossProfit(BaseProductForReportsView):
    template_name = 'reports/order_gross_profit.html'
    model = Order

    def get_queryset(self):
        pass

    def get_context_data(self, **kwargs):
        start, end = self.get_start_end_dates(self.request)
        if start or end is not None:
            new_qs = self.get_orders_with_range(start, end)
            date_range = end - start
            order_items = list()
            data = list()
            total = float()
            discount = 0
            payments_iterator = Payment.objects.filter(
                order__in=new_qs
            ).values(
                'payment_date', 'amount_paid', 'order_id'
            ).iterator()
            days = {}
            for item in payments_iterator:
                payment_date = item.get('payment_date').date()
                days.setdefault(payment_date, [])
                days[payment_date].append(item)
            for day in days:
                day_items = OrderItem.objects.filter(
                    order__in=new_qs.filter(close_date__startswith=day),
                    void_status__isnull=True)
                day_discount = day_items.aggregate(sum=Sum('discount')).values()
                order_items.extend(list(day_items))
                total += sum([payment.get('amount_paid') for payment in days[day]])
                if new_qs:
                    data.append({
                        'date': day.strftime('%B, %d'),
                        'info': {
                            'len': len(order_items),
                            'profit': sum(
                                ((i.price - i.discount) * i.quantity) - (i.cost * i.quantity) for i in order_items),
                            'total_sales': total,
                            'cost_of_goods_sold': sum(item.cost * item.quantity for item in order_items),
                            'discount': day_discount[0] if day_discount else 0
                        }
                    })
            return {'data': data, 'start_date': start.strftime('%B %d, %Y'),
                    'end_date': end.strftime('%B %d, %Y')}
        else:
            return {}


class EditEmployeeTotalHourSummaryReport(BaseProductForReportsView):
    model = Employee
    template_name = 'reports/edit_employee_total_hour.html'

    def get_queryset(self):
        pass

    # def get(self, request, *args, **kwargs):
    # print kwargs['pk']
    #
    #     return render(request, self.template_name)

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        start, end = BaseProductForReportsView.get_start_end_dates(self.request, True)
        employee = self.model.objects.exclude(archived=True).get(pk=pk)
        date_range = end - start
        result = dict()
        days = list()
        for day in range(date_range.days + 1):
            date = start + datetime.timedelta(days=day)
            days.append(date.strftime('%a, %d, %B'))
        # for employee in employees:
        week_list = list()
        total = datetime.timedelta(0)
        employee_hours = list()
        for day in range(date_range.days + 1):
            date = start + datetime.timedelta(days=day)
            next_day = date + datetime.timedelta(days=1)
            employee_time_clock = employee.time_clock.filter(time_in__range=(date, next_day)).exclude(archived=True)
            employee_hours.append(employee_time_clock)
            timedeltas = list()
            for emp in employee_time_clock:
                try:
                    timedeltas.append(emp.time_range())
                except:
                    pass
            summary = sum(timedeltas, datetime.timedelta(0))
            total += summary
            week_list.append(str(summary))
        try:
            pay_amount = float(total.seconds) / 3600 * float(employee.hourly_rate)
        except:
            pay_amount = 0.00
        result[employee.name] = {
            'hour_list': week_list,
            'total': str(total),
            'pay_amount': pay_amount,
            'employee_time_clock': employee_hours
        }
        store = product_models.Store.objects.get(pk=1)
        tz = store.timezone
        return {'result': result, 'days': days, 'employee': employee, 'pk': pk, 'tz': tz,
                'start_date': start.strftime('%B %d, %Y'),
                'end_date': end.strftime('%B %d, %Y')}


class EmployeeTotalHourSummaryReport(BaseProductForReportsView):
    model = Employee
    template_name = 'reports/employee_total_hour.html'

    def get_queryset(self):
        pass

    def get_context_data(self, **kwargs):
        start, end = self.get_start_end_dates(self.request, True)
        employees = self.model.objects.all().exclude(archived=True)
        date_range = end - start
        result = dict()
        days = list()
        for day in range(date_range.days + 1):
            date = start + datetime.timedelta(days=day)
            days.append(date.strftime('%a, %d, %B'))
        for employee in employees:
            week_list = list()
            total = datetime.timedelta(0)
            for day in range(date_range.days + 1):
                date = start + datetime.timedelta(days=day)
                next_day = date + datetime.timedelta(days=1)
                employee_time_clock = employee.time_clock.filter(time_in__range=(date, next_day)).exclude(archived=True)
                timedeltas = list()
                for emp in employee_time_clock:
                    timedeltas.append(emp.time_range())
                summary = sum(timedeltas, datetime.timedelta(0))
                total += summary
                week_list.append(str(summary))
            try:
                pay_amount = float(total.seconds) / 3600 * float(employee.hourly_rate)
            except:
                pay_amount = 0.00
            result[employee.name] = {
                'id': employee.id,
                'hour_list': week_list,
                'total': str(total),
                'pay_amount': pay_amount
            }
        store = product_models.Store.objects.get(pk=1)
        tz = store.timezone
        return {'result': result, 'days': days, 'tz': tz,
                'start_date': start.strftime('%B %d, %Y'),
                'end_date': end.strftime('%B %d, %Y'),}


class OrderTypesReport(BaseProductForReportsView):
    model = Order
    template_name = 'reports/order_types.html'

    def get_queryset(self):
        pass

    def get_context_data(self, **kwargs):
        start, end = self.get_start_end_dates(self.request)
        qs = self.get_orders_with_range(start, end, True)
        open_orders = qs.filter(status=1)
        held_orders = qs.filter(status=2)
        closed_orders = qs.filter(status=3)
        cancelled_orders = qs.filter(status=4)
        refunded_orders = qs.filter(status=5)
        return {
            'open_orders': {
                'number': len(open_orders),
                'total': open_orders.aggregate(sum=Sum('grand_total'))['sum']
            },
            'held_orders': {
                'number': len(held_orders),
                'total': held_orders.aggregate(sum=Sum('grand_total'))['sum']
            },
            'closed_orders': {
                'number': len(closed_orders),
                'total': closed_orders.aggregate(sum=Sum('grand_total'))['sum']
            },
            'cancelled_orders': {
                'number': len(cancelled_orders),
                'total': cancelled_orders.aggregate(sum=Sum('grand_total'))['sum']
            },
            'refunded_orders': {
                'number': len(refunded_orders),
                'total': refunded_orders.aggregate(sum=Sum('grand_total'))['sum']
            },
        }


@decorators.dispatch_decorator(login_required)
class TopCustomersView(BaseProductForReportsView):
    model = Order
    template_name = 'reports/top_customer.html'

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        start, end = BaseProductForReportsView.get_start_end_dates(self.request)
        qs = self.get_orders_with_range(start, end, True).exclude(customer__isnull=True).all()
        list_customer = list(qs)
        top_cutomers = dict()

        for lst in list_customer:
            if lst.customer_id in top_cutomers:
                customer = top_cutomers[lst.customer_id]
                customer.total_sum += lst.grand_total
                customer.total_transactions += 1
                top_cutomers[lst.customer_id] = customer
            else:
                setattr(lst.customer, 'total_sum', lst.grand_total)
                setattr(lst.customer, 'total_transactions', 1)
                top_cutomers[lst.customer_id] = lst.customer
        out = list()
        for key in top_cutomers:
            out.append(top_cutomers[key])
        out.sort(reverse=True, key=lambda x: x.total_sum)
        return {'top_cutomers': out,
                'start_date': start.strftime('%B %d, %Y'),
                'end_date': end.strftime('%B %d, %Y'),}


@decorators.dispatch_decorator(login_required)
class CheckOrdderMatch(cbv.ListView):
    model = OrderItem
    template_name = 'reports/checkordermatch.html'

    def get_context_data(self, **kwargs):
        qs = self.model.objects.filter(product_id__isnull=True)
        total = qs.count()
        withoutmatch = list()
        for item in qs:
            if item.name == 'Misc Item':
                product = product_models.Product.objects.get(id=-1)
                item.product_id = product
                item.save()
            elif item.name == 'Lottery Sale':
                product = product_models.Product.objects.get(id=14270)
                item.product_id = product
                item.save()
            elif item.name == 'Scratch Off':
                product = product_models.Product.objects.get(id=14271)
                item.product_id = product
                item.save()
            else:
                # try:
                product = product_models.Product.objects.filter(name=item.name, price=item.price).all()
                if product:
                    for product in product[:1]:
                        item.product_id = product
                else:
                    product = product_models.Product.objects.filter(name=item.name).all()
                    if product:
                        for product in product[:1]:
                            item.product_id = product
                    else:
                        withoutmatch.append(item)
                        product = product_models.Product.objects.get(id=-1)
                        item.product_id = product

                item.save()
        return {
            'totalforwork': total,
            'withoutmatch': withoutmatch
        }


class DiscountedOrdersView(BaseProductForReportsView):
    model = Order
    template_name = 'reports/discounted_orders.html'

    def get_queryset(self):
        pass

    def get_context_data(self, **kwargs):
        start, end = BaseProductForReportsView.get_start_end_dates(self.request)
        qs = self.get_orders_with_range(start, end).exclude(discount_total=0)
        return {'orders': qs, 'total': qs.count(),
                'start_date': start.strftime('%B %d, %Y'),
                'end_date': end.strftime('%B %d, %Y'),}


class GetSalesAndOrdersDashboard(BaseProductForReportsView):
    model = Order

    def render_to_response(self, context):
        return self.render_to_json_response(context)

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        start, end = self.get_start_end_dates(self.request)
        start = start - datetime.timedelta(days=14)
        if start is not None or end is not None:
            qs = self.get_orders_with_range(start, end)
            sorted_qs = sorted(qs, key=lambda x: x.open_date)

            date_range_grand_total = list()
            date_range_amount_total = list()
            categories = list()
            date_range = end - start

            for day in range(date_range.days + 1):
                date = start
                day_split_by_hours = list()

                # for hour in range(hours):
                time = date + datetime.timedelta(days=day)
                next_hour = time + datetime.timedelta(days=1)
                orders = filter(lambda x: time < x.close_date < next_hour, sorted_qs)

                amount = len(orders)
                sales = round(sum(order.grand_total for order in orders), 2)
                if amount > 0:
                    categories.append(time.strftime("%b,%a %d"))
                    date_range_grand_total.append(sales)
                    date_range_amount_total.append(amount)
            return {
                'categories': categories,
                'date_range_grand_total': date_range_grand_total,
                'date_range_amount_total': date_range_amount_total
            }
        else:
            return {}


@decorators.dispatch_decorator(login_required)
class CustomerReport(BaseProductForReportsView):
    template_name = 'reports/customer-report.html'

    model = Customer

    def get_queryset(self):
        pass

    def get_context_data(self, **kwargs):
        start, end = self._get_date_range()
        customer_id = self.request.GET.get('customer')
        terminal_id = self.request.GET.get('terminal')
        filter_orders = False

        if start is not None and end is not None:
            filter_orders = True

        # We need a distinct here in order to prevent duplicated customers. Also this improve the performance
        customers = Customer.objects.select_related('orders').filter(orders__isnull=False).distinct()
        customers_data = map(lambda c: {'name': c.get_full_name(),
                                        'id': c.id,
                                        'selected': True if customer_id is not None and
                                        int(customer_id) == c.id else False},
                             list(customers))

        terminals = Terminal.objects.all()
        terminals_data = map(lambda c: {'name': c.get_name(),
                                        'id': c.id,
                                        'selected': True if terminal_id is not None and
                                        int(terminal_id) == c.id else False},
                             list(terminals))
        if customer_id is not None:
            customers = customers.filter(pk=customer_id)
        if terminal_id:
            terminals = terminals.filter(pk=terminal_id)

        if filter_orders:
            if terminal_id:
                customers = customers.extra(select={
                    "bal": """
                    SELECT SUM(balance_remaining) FROM order_order
                    WHERE order_order.terminal_id = %d
                    AND order_order.open_date BETWEEN '%s' AND '%s'
                    AND order_order.customer_id = employees_customer.id
                    """ % (int(terminal_id), start, end,),
                })
                for customer in customers:
                    setattr(customer,
                            'report_orders',
                            list(customer.orders.filter(terminal_id=terminal_id, hold_date__gte=start, hold_date__lte=end)))

            else:
                customers = customers.extra(select={
                    "bal": """
                    SELECT SUM(balance_remaining) FROM order_order
                    WHERE order_order.open_date BETWEEN '%s' AND '%s'
                    AND order_order.customer_id = employees_customer.id
                    """ % (start, end),
                })
                for customer in customers:
                    setattr(customer,
                            'report_orders',
                            list(customer.orders.filter(hold_date__gte=start, hold_date__lte=end)))
        else:
            customers = customers.annotate(bal=Sum('orders__balance_remaining'))
            if terminal_id is not None:
                for customer in customers:
                    setattr(customer, 'report_orders', list(customer.orders.filter(terminal_id=terminal_id)))
            else:
                for customer in customers:
                    setattr(customer, 'report_orders', list(customer.orders.all()))
        if terminal_id is not None:
            for cu in customers:
                summ = 0
                orders_qs = cu.orders.filter(terminal_id=terminal_id)
                if filter_orders:
                    orders_qs = orders_qs.filter(terminal_id=terminal_id, hold_date__gte=start, hold_date__lte=end)
                orders = list(orders_qs)
                for order in orders:
                    if order.status == 3 or order.status == 4:
                        pass
                    else:
                        summ += order.grand_total
                setattr(cu, 'bal', summ)
        else:
            for cu in customers:
                summ = 0
                orders_qs = cu.orders.all()
                if filter_orders:
                    orders_qs = orders_qs.filter(hold_date__gte=start, hold_date__lte=end)
                orders = list(orders_qs)
                for order in orders:
                    if order.status == 3 or order.status == 4:
                        pass
                    else:
                        summ += order.grand_total
                setattr(cu, 'bal', summ)

        start_d = start.strftime('%B %d, %Y')
        end_d = end.strftime('%B %d, %Y')

        return {'customers': customers, 'dropdown_customers': customers_data, 'dropdown_terminals': terminals_data,
                'bal': cu.bal if customers else 0,
                'start_date': start_d,
                'end_date': end_d,
                }

    def _get_date_range(self):
        start = self.request.GET.get('start')
        end = self.request.GET.get('end')

        if start is not None and end is not None:
            start = datetime.datetime.strptime(start, '%B%d,%Y%I:%M%p')
            end = datetime.datetime.strptime(end, '%B%d,%Y%I:%M%p')

        if start is None and end is None:
            start = datetime.date.today().strftime('%B%d,%Y%I:%M%p')
            end = datetime.date.today().strftime('%B%d,%Y%I:%M%p')
            start, end = time.strptime(start, '%B%d,%Y%I:%M%p'), time.strptime(end, '%B%d,%Y%I:%M%p')
            start, end = datetime.datetime.fromtimestamp(time.mktime(start)),\
                         datetime.datetime.fromtimestamp(time.mktime(end))

        return start, end


@decorators.dispatch_decorator(login_required)
class HomeReportsView(cbv.TemplateView):
    template_name = 'reports/home.html'

    def get_context_data(self, **kwargs):
        return {'saved_url': ''}


class PayoutsView(BaseProductForReportsView):
    model = Shift
    template_name = 'reports/payouts.html'

    def get_queryset(self):
        start, end = self.get_start_end_dates(self.request)
        qs = self.model.objects.filter(
            Q(shift_open_date__range=(start, end)) | Q(shift_close_date__range=(start, end))).exclude(
            shift_close_date__gt=end)
        return qs


class PriceAdjustments(BaseProductForReportsView):
    model = Order

    template_name = 'reports/price_adjustments.html'

    def get_queryset(self):
        pass

    def get_context_data(self, **kwargs):
        start, end = BaseProductForReportsView.get_start_end_dates(self.request)
        qs = self.get_orders_with_range(start, end)
        out = []
        total_count = 0
        total_original = 0
        total_adjusted = 0
        total_difference = 0
        for order in qs:
            items = order.items.all()
            for item in items:
                if item.price != item.product.price:
                    difference = item.product.price - item.price
                    out.append((item, item.quantity, item.price, item.product.price, difference))
                    total_count += item.quantity
                    total_original += item.price
                    total_adjusted += item.product.price
                    total_difference += difference
        return {'out': out, 'total_count': total_count, 'total_original': total_original,
                'total_difference': total_difference, 'total_adjusted': total_adjusted,
                'start_date': start.strftime('%B %d, %Y'),
                'end_date': end.strftime('%B %d, %Y'),
                }


class ProductViewOrders(BaseProductForReportsView):
    template_name = 'reports/product_order_views.html'
    model = Order
    paginate_by = 50

    def get_queryset(self):
        start, end = BaseProductForReportsView.get_start_end_dates(self.request)
        qs = self.get_orders_with_range(start, end)
        qs = qs.filter(items__product__pk=self.kwargs['pk'])
        qs = qs.exclude(items__void_status=1)
        qs = qs.annotate(items_qty=Sum('items__quantity'))
        qs = qs.order_by('-close_date', '-open_date', '-id')
        return qs

    def get_context_data(self, **kwargs):
        start, end = BaseProductForReportsView.get_start_end_dates(self.request)
        context = super(ProductViewOrders, self).get_context_data()
        context["product"] = Product.objects.get(pk=self.kwargs['pk'])
        context['custom_product'] = int(self.kwargs['pk']) == -1
        context["product_orders"] = True
        context['start_date'] = start.strftime('%B %d, %Y')
        context['end_date'] = end.strftime('%B %d, %Y')
        return context


class TimeCardWeeklyReport(BaseProductForReportsView):
    model = Employee
    template_name = 'reports/time_card_weekly.html'

    def get_queryset(self):
        pass

    def get_context_data(self, **kwargs):
        WRAP_AT = 4
        context = super(TimeCardWeeklyReport, self).get_context_data()
        start, end = self.get_start_end_dates(self.request, True)
        employees = self.model.objects.all().exclude(archived=True)
        context['employees'] = []
        for emp in employees:
            xemployee = {
                'start': start,
                'end': end,
                'name': emp.name,
                'report': [],
                'total': 0.0,
            }
            day = start
            while day <= end:
                next_day = day + datetime.timedelta(days=1)
                employee_time_clock = \
                    emp.time_clock.filter(time_in__range=(day, next_day)). \
                    exclude(archived=True).order_by('time_in')
                for tc in employee_time_clock:
                    hours = 1.0 * tc.time_range().seconds / 3600
                    tin = tc.time_in.astimezone(day.tzinfo) if tc.time_in else tc.time_in
                    tout = tc.time_out.astimezone(day.tzinfo) if tc.time_out else tc.time_out
                    timezone.activate(tin.tzinfo)
                    xemployee['report'].append({
                        'date': day,
                        'tin': tin,
                        'tout': tout,
                        'hours': hours,
                    })
                    xemployee['total'] += hours
                if not employee_time_clock:  # empty day
                    xemployee['report'].append({
                        'date': day,
                        'tin': '',
                        'tout': '',
                        'hours': '',
                    })
                day = next_day
            context['employees'].append(xemployee)
        while len(context['employees']) % WRAP_AT != 0:
            context['employees'].append('-EMPTY-')
        context['saved_url'] = self.get_saved_time_period(self, False)
        context['start'] = start
        context['end'] = end
        context['wrap_at'] = WRAP_AT
        context['wrap_at_page'] = WRAP_AT * 2  # 2 rows
        context['current_date'] = '?start=' + str(start) + '&end=' + str(end)
        context['start_date'] = start.strftime('%B %d, %Y')
        context['end_date'] = end.strftime('%B %d, %Y')
        return context


class TimeCardWeeklyPDFReport(PDFResponseMixin, TimeCardWeeklyReport):
    pdf_name = 'time_card_weekly'

    def get_template_names(self):
        return "reports/pdf/%s.html" % self.pdf_name


@decorators.dispatch_decorator(login_required)
class CustomerOrderAjaxView(cbv.View, JSONResponseMixin):
    def get_object(self):
        return get_object_or_404(Customer, id=self.kwargs.get("pk"))

    def get_queryset(self):
        obj = self.get_object()
        return obj.orders.filter(balance_remaining__gt=0).exclude(status__in=[4])

    def isolated_queryset(self):
        queryset = self.get_queryset()
        orders = []
        for obj in queryset:
            grand_total = obj.grand_total or "0.00"
            balance_remaining = obj.balance_remaining or "0.00"
            orders.append({
                "id": obj.id,
                "open_date": obj.open_date.strftime("%m-%d-%Y %I:%M %p"),
                "grand_total": intcomma(floatformat(grand_total, 2)),
                "balance_remaining": intcomma(floatformat(balance_remaining, 2))
            })
        return orders

    def serialize_queryset(self):
        queryset = self.get_queryset()
        orders = []
        for obj in queryset:
            grand_total = obj.grand_total or "0.00"
            balance_remaining = obj.balance_remaining or "0.00"
            orders.append({
                "id": obj.id,
                "open_date": obj.open_date.strftime("%m-%d-%Y %I:%M %p"),
                "grand_total": intcomma(floatformat(grand_total, 2)),
                "balance_remaining": intcomma(floatformat(balance_remaining, 2))
            })
        return orders

    def _get_total_values(self):
        orders = self.get_queryset()
        grand_total = orders.aggregate(sum=Sum('grand_total'))['sum'] or "0.00"
        balance_remaining = orders.aggregate(sum=Sum('balance_remaining'))['sum'] or "0.00"
        return {
            "grand_total": intcomma(floatformat(grand_total, 2)),
            "balance_remaining": intcomma(floatformat(balance_remaining, 2))
        }

    def get_context_data(self, **kwargs):
        context = {}
        context["orders"] = self.serialize_queryset()
        context["total"] = self._get_total_values()
        return context

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            context = self.get_context_data()
            return self.render_to_json_response(context)
        raise Http404


@decorators.dispatch_decorator(login_required)
class CustomerPaymentView(cbv.DetailView):
    template_name = 'reports/customer_payment.html'

    model = Customer

    def get_form_initials(self):
        customer = self.get_object()
        amount = Decimal("0.00"),
        payment_date = datetime.datetime.today()
        return {
            "customer": customer,
            "amount": amount,
            "payment_date": payment_date.strftime("%m-%d-%Y %I:%M %p")
        }

    def get_success_url(self):
        return reverse("customer_list")

    def post(self, request, *args, **kwargs):
        form = CustomerPaymentForm(request.POST)

        if form.is_valid():
            amount = form.cleaned_data.get("amount")
            payment_date = form.cleaned_data.get("payment_date")
            payment_method = form.cleaned_data.get("payment_method")
            check_number = form.cleaned_data.get("check_number")
            employee = form.cleaned_data.get("employee_id")
            custom_order = get_object_or_404(Order, id=-1)
            custom_terminal_id = get_object_or_404(Terminal, id=-1)

            if payment_method == 'Account':
                pr_response = "ACCOUNT"
            else:
                pr_response = "APPROVAL"

            main_payment = Payment.objects.create(
                order=custom_order,
                amount=amount,
                amount_paid=amount,
                change_amount=0,
                payment_type=payment_method,
                payment_date=payment_date,
                check_number=check_number,
                transaction_type=1,  # for "Sale" value
                processor_response=pr_response,
                terminal_id=custom_terminal_id.id,
                payment_form=str(payment_method).upper(),
                employee_id=request.user.id,

            )

            for key in request.POST.keys():
                if "balance_payment" in key:
                    order_id = int(key.split("_")[-1:][0])
                    payment = float(request.POST.get(key))

                    order = get_object_or_404(Order, id=order_id)
                    balance = order.balance_remaining - payment

                    if payment_method == 'Account':
                        pr_response = "ACCOUNT"
                    else:
                        pr_response = "APPROVAL"

                    Payment.objects.create(
                        order=order,
                        amount=payment,
                        amount_paid=payment,
                        change_amount=0,
                        payment_type=payment_method,
                        payment_date=payment_date,
                        transaction_type=1,  # for "Sale" value
                        processor_response=pr_response,
                        void_ref=main_payment.id,
                        check_number=check_number,
                        terminal_id=custom_terminal_id.id,
                        payment_form=str(payment_method).upper(),
                        employee_id=request.user.id,
                    )

                    order.balance_remaining = balance
                    if balance <= 0:
                        # of course it should be compared equally to 0, but who knows what was passed...
                        # close the order if balance is 0 now
                        order.status = 3
                    order.save()

            messages.success(request, _("Successfully processed a payment."))
            return http.HttpResponseRedirect(self.get_success_url())

        self.object = self.get_object()
        context = self.get_context_data()
        context["form"] = form
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(CustomerPaymentView, self).get_context_data()
        initials = self.get_form_initials()
        context["form"] = CustomerPaymentForm(initial=initials)
        return context
