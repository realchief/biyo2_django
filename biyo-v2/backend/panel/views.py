# -*- coding: utf-8 -*-
import csv
import datetime
import json
from types import NoneType

# from utils import get_object_or_None

import pytz
from django import http
from django import shortcuts
from django.contrib import messages
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Q, Sum, Prefetch, Count
from django.http.response import Http404, HttpResponseRedirect
from django.http import StreamingHttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import generic as cbv
from datetime import timedelta
from calendar import monthrange
from slugify import slugify
import sys

from django.views.generic.edit import UpdateView
from rest_framework import status

sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__

from employees import models as employees_models
from employees.forms import (EmployeeForm, CustomerForm, AddCustomerForm, EmployeeCreateForm,
                             ChangeEmpPass, CvsCustomerUploadForm, SupplierForm, AddSupplierForm)
from order.forms import *
from products import models as products_models
from products.forms import (ProductForm, ModifierForm, CategoryForm,
                            TableSectionForm, PrinterForm, TimeClockForm, RewardsForm,
                            QuickAddProductForm, CvsUploadForm, ProductCategoryForm,
                            OrderSortForm, ProductMultipleCategoryForm)
from products.models import TaxRate, Category, Product, Modifier, Store
from reports.views import BaseProductForReportsView
from taskin.models import CustomerGroup, SpecialPrices
from . import crud
from . import decorators
from django.forms.models import fields_for_model
from collections import defaultdict
from operator import itemgetter
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from django.http import HttpResponse


class LoginReqListView(cbv.ListView):
    form_model = None

    def get_queryset(self):
        qs = super(LoginReqListView, self).get_queryset()
        qs = qs.filter(archived=False)

        return qs

    pass


class InfoFieldsDetailView(cbv.DetailView):
    """
    Class based view for display detail object with info_fields
    """
    info_fields = None

    def get_context_data(self, **kwargs):
        context = super(InfoFieldsDetailView, self).get_context_data(**kwargs)
        context.update({'info_fields': self.info_fields})
        return context


class MessageObjectMixin(object):
    """
    Mixin for setting message
    """
    message = None
    message_pattern = None

    def set_message(self):
        LoggerUpdater.logR(self)
        if self.message is None:
            self.message = self.message_pattern % unicode(self.object)
        messages.success(
            self.request,
            self.message
        )


class DetailSuccessUrlMixin(object):
    """
    Return redirect to a list view
    """
    detail_url_name = None

    def get_success_url(self):
        split = self.detail_url_name.split('_')
        redirect_url = split[0] + '_list'
        return redirect_url


class LoggerUpdater(object):
    @staticmethod
    def logR(model):
        LogEntry.objects.log_action(
            user_id=model.request.user.id,
            content_type_id=ContentType.objects.get_for_model(model.object).pk,
            object_id=model.object.id,
            object_repr=unicode(model.object),
            change_message=model.log_message,
            action_flag=model.log_type
        )


class ModelFormWithMessageMixin(DetailSuccessUrlMixin, MessageObjectMixin):
    def form_valid(self, form):
        self.object = form.save()
        self.set_message()
        return shortcuts.redirect(self.get_success_url())


class MessageCreateView(ModelFormWithMessageMixin, cbv.CreateView):
    log_type = ADDITION
    log_message = 'New Item has been created'
    pass


class MessageUpdateView(ModelFormWithMessageMixin, cbv.UpdateView):
    log_type = CHANGE
    log_message = 'Object has been changed'

    def get_context_data(self, **kwargs):
        context = super(MessageUpdateView, self).get_context_data(**kwargs)
        tz = products_models.Store.objects.first().timezone
        tz = pytz.timezone(tz)
        context['tz'] = tz

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        name = request.POST.get('name')
        value = request.POST.get('value')
        tax_status = request.POST.get('tax_status')
        is_active = request.POST.get('active')
        switch = request.POST.get('switch')
        if request.is_ajax() and name and value:
            setattr(self.object, name, value)
            self.object.save()
            return shortcuts.redirect(self.get_success_url())
        elif request.is_ajax() and switch == 'moved':  # for switchers in product list
            if tax_status:
                state = json.loads(tax_status)
                if state:
                    state = 0
                else:
                    state = 1
            else:
                state = json.loads(is_active)
            setattr(self.object, 'tax_status' if tax_status else 'active', state)
            self.object.save()
            return HttpResponse("Success")
        else:
            return super(MessageUpdateView, self).post(request, *args, **kwargs)


class MessageDeleteView(MessageObjectMixin, crud.DeleteView):
    log_type = DELETION
    log_message = 'Object has been archived'
    success_url_name = None

    def get_success_url(self):
        return reverse(self.success_url_name)

    def post(self, request, *args, **kwargs):
        response = super(MessageDeleteView, self).post(
            request,
            *args,
            **kwargs
        )
        self.set_message()
        return response


@decorators.dispatch_decorator(login_required)
class DashboardView(cbv.TemplateView):
    template_name = 'dashboard.html'
    weekdays = {
        1: 'Mon',
        2: 'Tue',
        3: 'Wed',
        4: 'Thu',
        5: 'Fri',
        6: 'Sat',
        7: 'Sun'
    }

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        tz = products_models.Store.objects.first().timezone
        tz = pytz.timezone(tz)
        context['tz'] = tz
        context['total_orders'] = Order.objects.count()

        start, end = BaseProductForReportsView.get_start_end_dates(self.request)
        interval = end - start
        istart = start - interval
        iend = end - interval
        context['start_date'] = start.strftime('%B %d, %Y')
        context['end_date'] = end.strftime('%B %d, %Y')
        # Count the number of customer that have creation date of today
        try:
            new_customers = employees_models.Customer.objects.filter(created__gte=start).count()
        except Exception:
            new_customers = 0
        context['new_customers'] = new_customers
        returned_customers = employees_models.Customer.objects.filter(orders__close_date__gte=start,
                                                                      created__lte=start).distinct().all().count()
        context['returned_customers'] = returned_customers

        if context['total_orders']:
            context['avg_order_value'] = \
                Order.objects.aggregate(Sum('grand_total'))['grand_total__sum'] / float(context['total_orders'])
        else:
            context['avg_order_value'] = 0
        context['last_seven_orders'] = Order.objects.all().order_by('-id')[:10]

        today_order = Order.objects.filter(open_date__gte=start, status=3)
        itoday_order = Order.objects.filter(Q(open_date__range=(istart, iend), status=3))

        if itoday_order.count() != 0 and today_order.count() != 0:
            context['proc_orders'] = float(today_order.count()) * 100 / float(itoday_order.count()) - 100
        else:
            if itoday_order.count() == 0 and today_order.count() != 0:
                context['proc_orders'] = 100
            if itoday_order.count() != 0 and today_order.count() == 0:
                context['proc_orders'] = -100

        context['todays_orders_count'] = today_order.count()
        context['itodays_orders_count'] = itoday_order.count()

        context['todays_sales'] = today_order.aggregate(Sum('grand_total'))['grand_total__sum']
        context['itodays_sales'] = itoday_order.aggregate(Sum('grand_total'))['grand_total__sum']

        if context['todays_sales'] != None and context['itodays_sales'] != None:
            context['proc_sales'] = float(context['todays_sales']) * 100 / float(context['itodays_sales']) - 100
        else:
            if context['itodays_sales'] == None and context['todays_sales'] != None:
                context['proc_sales'] = 100
            if context['itodays_sales'] != None and context['todays_sales'] == None:
                context['proc_sales'] = -100

        if context['todays_orders_count'] or context['itodays_orders_count']:
            if context['todays_orders_count']:
                context['todays_average_sales'] = float(context['todays_sales']) / float(context['todays_orders_count'])
                if context['itodays_sales'] != None:
                    context['itodays_average_sales'] = float(context['itodays_sales']) / float(context['itodays_orders_count'])
                    if context['itodays_average_sales'] != None:
                        if context['todays_average_sales'] != None:
                            context['proc_av_sales'] = float(context['todays_average_sales']) * 100 / float(context['itodays_average_sales']) - 100
                else:
                    context['proc_av_sales'] = 100
            else:
                context['proc_av_sales'] = -100
        orders = BaseProductForReportsView.get_orders_with_range(start, end)
        # orders = Order.objects.all()
        items = OrderItem.objects.filter(order__in=orders).exclude(void_status=1)
        qs = items.values('product__name', 'product_id', 'product__barcode').annotate(amount=Sum('price')).order_by(
            '-amount',
            'product__name'
        )
        top_three_product = qs[:3]
        current_url = '?start=' + start.strftime('%B%d,%Y12:00AM') + '&end=' + end.strftime('%B%d,%Y11:59PM') + '&option=0'
        context['top_product'] = top_three_product
        context['saved_url'] = current_url
        context['sale_statistic'] = self.build_sale_statistic(interval, start, end, orders)
        context['week_sales_summary'] = self.build_day_of_week_statistic()
        context['day_sales_summary'] = self.build_time_of_day_statistic()
        context['payment_methods'] = self.payment_methods_statistic()
        context['top_categories'] = self.top_categories()

        return context

    def build_sale_statistic(self, interval, start, end, orders):
        sale_statistic = []
        if interval.days < 2:
            for hour in xrange(0, 24):
                grand_total = orders.extra(
                    where=['extract(hour from close_date) in (%s)' % hour]
                ).aggregate(Sum('grand_total'))
                sale_statistic.append({self.from_int_to_hour(hour): grand_total})
        elif interval.days <= 7:
            for single_date in self.daterange(start, end):
                sale_statistic.append(
                    {self.weekdays[single_date.isoweekday()]: orders.extra(
                    where=['extract(day from close_date) in (%s)' % single_date.day]
                    ).aggregate(Sum('grand_total'))}
                )
        elif interval.days <= 60:
            for single_date in self.daterange(start, end):
                sale_statistic.append(
                    {'{} {}'.format(single_date.date().strftime("%B"), single_date.date().day): orders.filter(
                        Q(close_date__gte=single_date),
                        Q(close_date__lte=single_date + timedelta(1))
                    ).aggregate(Sum('grand_total'))}
                )
        else:
            for year, month in self.month_year_iter(start.month , start.year, end.month, end.year):
                sale_statistic.append(
                    {
                        datetime(year, month, 1).date().strftime("%B") + " '" + str(year)[2:]: orders.filter(
                            Q(close_date__gte=datetime(year, month, 1)),
                            Q(close_date__lte=datetime(year, month, 1) + timedelta(monthrange(year, month)[1]))
                        ).aggregate(Sum('grand_total'))
                    }
                )
        return json.dumps(sale_statistic)

    def build_day_of_week_statistic(self):
        week_sales_summary = []
        today = datetime.today()
        orders = Order.objects.filter(close_date__gte=datetime.today().date() - timedelta(7))
        for single_date in self.daterange(today - timedelta(7), today):
            # day_sum = orders.filter(close_date__day=single_date.day).aggregate(Sum('grand_total'))

            #  IF DJANGO FILTER WILL NOT WORK ON MYSQL DB THEN USE THIS RAW SQL
            day_sum = orders.raw(
                "SELECT order_order.id, SUM(order_order.grand_total) "
                "FROM order_order WHERE "
                "(order_order.close_date >= '{}' AND "
                "EXTRACT(DAY FROM order_order.close_date) = '{}') GROUP BY "
                "order_order.id".format(today - timedelta(7), single_date.day)
            )
            try:
                day_sum = day_sum[0]
                day_sum = getattr(day_sum, 'SUM(order_order.grand_total)')
            except IndexError:
                continue

            week_sales_summary.append(
                {self.weekdays[single_date.isoweekday()]: "%.2f" % float(day_sum or 0)}
            )
        return json.dumps(week_sales_summary)

    def build_time_of_day_statistic(self):
        day_sales_summary = []
        sales = Order.objects.extra(
            {'HOUR': 'extract(HOUR from close_date)'}
        ).values('HOUR').annotate(sum=Sum('grand_total')).order_by('HOUR')
        for sale in sales:
            hour = sale.get("HOUR")
            hour_sum = sale.get("sum")
            if hour is not None:
                day_sales_summary.append({self.from_int_to_hour(hour) if hour % 2 else '': hour_sum or 0})
        return json.dumps(day_sales_summary)

    def payment_methods_statistic(self):
        payment_methods = Payment.objects.values('payment_type').annotate(count=Sum('amount_paid'))
        return json.dumps(
            [
                {'{} - ${}'.format(method['payment_type'], method['count']): method['count']}
                for method in payment_methods
                ]
        )

    def top_categories(self):
        categories_sales = OrderItem.objects.filter(
            order_id__in=Payment.objects.filter(
                order__status=3
            )
        ).values('product__categories__name').annotate(
            categories_sales=Sum('price')
        ).order_by('-categories_sales')[:7]
        categories_list = [
            {
                obj.get('product__categories__name'): obj.get('categories_sales')
            } for obj in categories_sales
            ]
        return categories_list

    def month_year_iter(self, start_month, start_year, end_month, end_year):
        ym_start = 12 * start_year + start_month
        ym_end = 12 * end_year + end_month
        for ym in range(ym_start, ym_end):
            y, m = divmod(ym, 12)
            yield y, m + 1

    def from_int_to_hour(self, hour):
        hr = datetime.strptime(str(hour), "%H")
        return hr.strftime("%I:%M %p")

    def daterange(self, start_date, end_date):
        for n in xrange(int((end_date - start_date).days)):
            yield start_date + timedelta(n)

def OrderSortListClean(request):
    if 'status' in request.session:
        del request.session['status']
    if 'employee' in request.session:
        del request.session['employee']
    if 'payment' in request.session:
        del request.session['payment']
    if 'terminal' in request.session:
        del request.session['terminal']
    return shortcuts.redirect('order-list')


@decorators.dispatch_decorator(login_required)
class OrderListView(BaseProductForReportsView):
    model = Order
    template_name = 'order_list.html'
    paginate_by = 25

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        tz = products_models.Store.objects.first().timezone
        tz = pytz.timezone(tz)

        try:
            start, end = self.get_start_end_dates(self.request)
            context = super(OrderListView, self).get_context_data(**kwargs)
            form = OrderSortForm(self.request)
            context['tz'] = tz
            context['form'] = form
            context['start_date'] = start.strftime('%B %d, %Y')
            context['end_date'] = end.strftime('%B %d, %Y')
            return context
        except Http404:
            self.kwargs['page'] = 1
            context = super(OrderListView, self).get_context_data(**kwargs)
            form = OrderSortForm(self.request)
            context['tz'] = tz
            context['form'] = form
            return context

    def get_queryset(self):
        queryset = Order.objects.all().\
            prefetch_related('emp_open', 'emp_close').\
            distinct()
        start, end = self.get_start_end_dates(self.request)
        from django.db.models import Q
        queryset = queryset.filter(Q(open_date__range=(start, end)) | Q(close_date__range=(start, end))).exclude(
            close_date__gt=end)
        queryset = queryset.exclude(items=None)  # do not show empty orders
        status = self.request.POST.get('status')
        if status:
            queryset = queryset.filter(status=status)
            self.request.session['status'] = status
        elif status == '':
            if 'status' in self.request.session:
                del self.request.session['status']
        elif 'status' in self.request.session:
            queryset = queryset.filter(status=self.request.session['status'])

        employee = self.request.POST.get('employees')
        if employee:
            self.request.session['employee'] = employee
            queryset = queryset.filter(emp_close_id=employee)
        elif employee == '':
            if 'employee' in self.request.session:
                del self.request.session['employee']
        elif 'employee' in self.request.session:
            queryset = queryset.filter(emp_close_id=self.request.session['employee'])

        payment = self.request.POST.get('payment')
        if payment:
            self.request.session['payment'] = payment
            if payment == 'allcards':
                paymentList = ('Visa', 'MasterCard', 'OtherCredit', 'American Express')
                queryset = queryset.filter(payments__payment_type__in=paymentList)
            else:
                queryset = queryset.filter(payments__payment_type=payment)
        elif payment == '':
            if 'payment' in self.request.session:
                del self.request.session['payment']
        elif 'payment' in self.request.session:
            if self.request.session['payment'] == 'allcards':
                paymentList = ('Visa', 'MasterCard', 'OtherCredit', 'American Express')
                queryset = queryset.filter(payments__payment_type__in=paymentList)
            else:
                queryset = queryset.filter(payments__payment_type=self.request.session['payment'])

        terminal = self.request.POST.get('terminal')
        if terminal:
            self.request.session['terminal'] = terminal
            queryset = queryset.filter(terminal_id=terminal)
        elif terminal == '':
            if 'terminal' in self.request.session:
                del self.request.session['terminal']
        elif 'terminal' in self.request.session:
            queryset = queryset.filter(terminal_id=self.request.session['terminal'])

        customer = self.request.POST.get('customer')
        if customer:
            self.request.session['customer'] = customer
            queryset = queryset.filter(customer_id=customer)
        elif terminal == '':
            if 'customer' in self.request.session:
                del self.request.session['customer']
        elif 'customer' in self.request.session:
            queryset = queryset.filter(customer_id=self.request.session['customer'])

        sorted_queryset = sorted(queryset, key=lambda x: x.id, reverse=True)
        return sorted_queryset


@decorators.dispatch_decorator(login_required)
class OrderDetailView(cbv.DetailView):
    model = Order
    template_name = 'order_detail.html'

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        order_items = self.object.items.all().exclude(void_status=1)
        voided_order_items = self.object.items.filter(void_status=1)
        customer = self.object.customer
        try:
            payment = Payment.objects.filter(order_id=self.object.id)
        except ObjectDoesNotExist:
            payment = None
        tz = products_models.Store.objects.first().timezone
        tz = pytz.timezone(tz)
        store = Store.objects.first()
        return {
            'object': self.object,
            'order_items': order_items,
            'voided_items': voided_order_items,
            'customer': customer,
            'payment': payment.first(),
            'tz': tz,
            'store': store
        }


@login_required
def change_password(request, pk):
    form = ChangeEmpPass(request.POST or None)
    if form.is_valid():
        user = get_object_or_404(employees_models.Employee, pk=pk)
        if user.check_password(form.cleaned_data['old_password']):
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            return render(request, 'success.html')
        else:
            return render(request, 'change_pass.html', {'error': 'You have entered wrong old password', 'form': form})

    return render(request, 'change_pass.html', {'form': form})


class ExtendModelCrud(crud.BaseModelCRUD):
    info_fields = None
    fields = None
    default_decorators = [login_required]
    created_message_pattern = '%s has been created'
    updated_message_pattern = '%s has been updated'
    delete_message_pattern = '%s has been deleted'
    list_class_view = LoginReqListView

    detail_class_view = InfoFieldsDetailView

    create_class_view = MessageCreateView
    update_class_view = MessageUpdateView
    delete_class_view = MessageDeleteView
    list_view_form = None

    def get_list_kwargs(self):
        return {
            'paginate_by': 50
        }

    def get_detail_kwargs(self):
        return {
            'info_fields': self.info_fields
        }

    def get_update_kwargs(self):
        return {
            'fields': self.fields,
            'message_pattern': self.updated_message_pattern,
            'detail_url_name': self.detail_url_name
        }

    def get_create_kwargs(self):
        return {
            'fields': self.fields,
            'message_pattern': self.created_message_pattern,
            'detail_url_name': self.detail_url_name
        }

    def get_delete_kwargs(self):
        return {
            'success_url_name': self.list_url_name,
            'message_pattern': self.delete_message_pattern
        }

    def get_form(self):
        return self.list_view_form


class ProductUpdateView(MessageUpdateView):
    form_class = ProductForm

    def get_context_data(self, **kwargs):
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        product = context['product']
        customergroup = CustomerGroup.objects.all()
        for group in customergroup:
            try:
                special = group.taskin_special_price_group.get(product=product)
                if special:
                    setattr(group, 'special', special.price)
            except SpecialPrices.DoesNotExist:
                pass
        context['customergroup'] = customergroup
        return context


class ProductCreateView(MessageCreateView):
    form_class = ProductForm

    # def get_context_data(self, **kwargs):
    #     categories = Category.objects.all()
    #     return super(ProductCreateView, self).get_context_data(categories=categories)


# TODO: Move to products app.
class ProductListView(LoginReqListView):
    form_model = ProductForm

    def get_context_data(self, **kwargs):
        try:
            context = super(ProductListView, self).get_context_data(**kwargs)
            context['category_form'] = ProductCategoryForm(self.request.POST)
            context['multiple_category_form'] = ProductMultipleCategoryForm()
            context['form'] = self.form_model
            context['sort_by'] = self.request.POST.get('sort_by')
            context['categories'] = Category.objects.exclude(archived=True)

            try:
                context['filter_tag'] = self.request.session['search_phrase']
            except KeyError:
                pass

            return context
        except Http404:
            self.kwargs['page'] = 1
            return super(ProductListView, self).get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        selected_category = self.request.POST.get('categories')
        if selected_category == "All categories":
            selected_category = None
        self.object_list = self.get_queryset(selected_category=selected_category)
        context = self.get_context_data()
        context['filter_tag'] = self.request.POST.get('filter_tag')
        context['selected_category'] = int(selected_category) if selected_category else selected_category
        return self.render_to_response(context)

    def get_queryset(self, **kwargs):
        qs = super(LoginReqListView, self).get_queryset()
        sort_by = self.request.POST.get('sort_by')
        category = kwargs.get('selected_category')

        search_phrase = self.request.POST.get('filter_tag', '')
        prefetch = Prefetch(
            'categories',
            queryset=Category.objects.all()
            .select_related('product'), to_attr='category_prods'
        )
        qs = qs.prefetch_related(prefetch)

        if not sort_by:
            sort_by = "name"
        if category and not category == 'None':
            qs = qs.filter(categories=category)
        # ***********************************
        if 'search_phrase' in self.request.session:
            if search_phrase and self.request.session['search_phrase'] != search_phrase:
                self.request.session['search_phrase'] = search_phrase
            else:
                search_phrase = self.request.session['search_phrase']
        elif search_phrase:
            self.request.session['search_phrase'] = search_phrase
        if search_phrase:
            qs = qs.filter(Q(name__icontains=search_phrase) | Q(barcode__icontains=search_phrase))
        # ***********************************
        qs = qs.filter(archived=False).exclude(id=-1).order_by(sort_by)
        self.request.session['result_qs'] = unicode(qs.query)
        return qs


class ProductExportCsvView(ProductListView):
    model = Product

    def get(self, request, *args, **kwargs):
        return shortcuts.redirect('product_list')

    def post(self, request, *a, **kw):
        ENCODING = sys.stdout.encoding if sys.stdout.encoding else 'utf-8'
        self.object_list = self.get_queryset().prefetch_related('categories')
        header = ['id', ] + fields_for_model(Product).keys()
        header.remove('change_reason')
        header.remove('modifier_groups')
        header.remove('stock_change')

        values = self.object_list.values(*header)
        categories = []
        for obj in self.object_list:
            categories.append(
                {
                    'categories': ','.join(obj.categories.values_list('name', flat=True)),
                    'id': obj.id
                }
            )

        response = defaultdict(dict)
        for dicts in (values, categories):
            for elem in dicts:
                if "image" in elem:
                     elem["image"] = elem["image"].encode(ENCODING)
                if elem.get('description'):
                    elem['description'] = slugify(elem['description'])
                if elem.get('name'):
                    elem['name'] = slugify(elem['name'])
                response[elem['id']].update(elem)
        response = sorted(response.values(), key=itemgetter('id'))
        f = StringIO()
        dwriter = csv.DictWriter(f, fieldnames=header)
        dwriter.writeheader()
        dwriter.writerows(response)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=product.csv'
        response.write(f.getvalue())
        return response


# XXX: Remove after close ticket #5193411
class Echo(object):

     def write(self, value):
         """Write the value by returning it, instead of storing in a buffer."""
         return value
#
#
# class ProductExportCsvView(LoginReqListView):
#     def get(self, request, *args, **kwargs):
#         raw_query = list(request.session['result_qs'])
#         a = 0
#         for i, j in enumerate(raw_query):
#             if j == '%' and a == 0:
#                 raw_query[i] = '"%%'
#                 a += 1
#             elif j == '%' and a == 1:
#                 raw_query[i] = '%%"'
#                 a += 1
#             elif j == '%' and a == 2:
#                 raw_query[i] = '"%%'
#                 a += 1
#             elif j == '%' and a == 3:
#                 raw_query[i] = '%%"'
#
#         y = "".join(raw_query)
#         qs = Product.objects.raw(str(y.encode('utf-8')))
#         model = qs.model
#         model_fields = model._meta.fields + model._meta.many_to_many
#         headers = [field.name for field in model_fields]  # Create CSV headers
#
#         def get_row(obj):
#             row = []
#             for field in model_fields:
#                 if type(field) == models.ForeignKey:
#                     val = getattr(obj, field.name)
#                     if val:
#                         val = val.__unicode__()
#                 elif type(field) == models.ManyToManyField:
#                     val = u', '.join([item.__unicode__() for item in getattr(obj, field.name).all()])
#                 elif field.choices:
#                     val = getattr(obj, 'get_%s_display' % field.name)()
#                 else:
#                     val = getattr(obj, field.name)
#                 row.append(unicode(val).encode("utf-8"))
#             return row
#
#         def stream(headers, data):  # Helper function to inject headers
#             if headers:
#                 yield headers
#             for obj in data:
#                 yield get_row(obj)
#
#         pseudo_buffer = Echo()
#         writer = csv.writer(pseudo_buffer)
#
#         response = StreamingHttpResponse(
#             (writer.writerow(row) for row in stream(headers, qs)),
#             content_type="text/csv")
#
#         response['Content-Disposition'] = 'attachment; filename="product.csv"'
#         return response


class ClearFilterProduct(LoginReqListView):
    def get(self, request, *args, **kwargs):
        request.session.modified = True
        if 'search_phrase' in request.session:
            del request.session['search_phrase']
        return HttpResponseRedirect(reverse('product_list'))


class PrinterUpdateView(MessageUpdateView):
    form_class = PrinterForm


class PrinterCreateView(MessageCreateView):
    form_class = PrinterForm


class PrinterListView(LoginReqListView):
    form_model = PrinterForm

    def get_context_data(self, **kwargs):
        return {'object_list': self.get_queryset(), 'form': self.form_model}


class TimeClockUpdateView(MessageUpdateView):
    form_class = TimeClockForm

    def get_success_url(self):
        return reverse('edit_employee_hour_summary', kwargs={'pk': self.object.employee_id})


class TimeClockCreateView(MessageCreateView):
    form_class = TimeClockForm

    def get_success_url(self):
        return reverse('edit_employee_hour_summary', kwargs={'pk': self.object.employee_id})


class TimeDeleteView(MessageDeleteView):
    def get_success_url(self):
        return reverse('edit_employee_hour_summary', kwargs={'pk': self.object.employee_id})


class TimeClockCrud(ExtendModelCrud):
    update_class_view = TimeClockUpdateView
    create_class_view = TimeClockCreateView
    # list_class_view = TimeClockListView
    delete_class_view = TimeDeleteView


class PrinterCrud(ExtendModelCrud):
    update_class_view = PrinterUpdateView
    create_class_view = PrinterCreateView
    list_class_view = PrinterListView


printer_crud = PrinterCrud(
    model=products_models.Printer,
    fields=('name', 'local_ip'),
    info_fields=('id', 'name', 'local_ip'),
)

time_crud = TimeClockCrud(
    model=employees_models.TimeClock,
    fields=('time_in', 'time_out'),
    info_fields=('id', 'employee', 'time_in', 'time_out')
)


class ProductCrud(ExtendModelCrud):
    update_class_view = ProductUpdateView
    create_class_view = ProductCreateView
    list_class_view = ProductListView

    @decorators.return_detail_view
    def add_category(self):
        def view(request, pk):
            return http.HttpResponse(content="Add category for %s" % pk)

        return view

    @decorators.return_detail_view
    def del_category(self):
        def view(request, pk):
            return http.HttpResponse(content="Add category for %s" % pk)

        return view

    @decorators.return_detail_view
    def add_modifier_group(self):
        def view(request, pk):
            return http.HttpResponse(content='Add modifier group for %s' % pk)

        return view

    @decorators.return_detail_view
    def del_modifier_group(self):
        def view(request, pk):
            return http.HttpResponse(content='Del modifier group for %s' % pk)

        return view


product_crud = ProductCrud(
    model=products_models.Product,
    info_fields=('name', 'description', 'price', 'cost', 'color', 'barcode', 'stock',
                 'tax_rate', 'tax_status', 'active', 'price_adjust', 'print_to', 'printer'),
)


class ModifierGroupUpdateView(MessageUpdateView):
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.is_ajax():
            if request.POST.get('name') == 'select_multiple':
                value = False
                if request.POST.get('value') == 'True':
                    value = True
                self.object.select_multiple = value
            elif request.POST.get('name') == 'group':
                for id in dict(request.POST)['value[]']:
                    self.object.group.clear()
                    self.object.group.add(products_models.ModifierGroup.objects.get(pk=id))
            else:
                setattr(self.object, request.POST.get('name'), request.POST.get('value'))
            self.object.save()
            return shortcuts.redirect(self.get_success_url())
        return super(MessageUpdateView, self).post(request, *args, **kwargs)


class ModifierGroupListView(LoginReqListView):
    def get_context_data(self, **kwargs):
        context = dict()
        context['object_list'] = self.get_queryset()
        context['form'] = self.form_model
        context['moditems'] = Modifier.objects.filter(archived=False)
        return context


class ModifierGroupDetailView(LoginReqListView):
    """
    Class based view for display detail object with info_fields
    """
    info_fields = None
    template_name = 'modifiergroup_list.html'

    def get_context_data(self, **kwargs):
        context = super(ModifierGroupDetailView, self).get_context_data(**kwargs)
        pk = self.kwargs['pk']
        modItems = self.model.objects.filter(id=pk, archived=False).select_related("modifiers").get().modifiers.filter(
            archived=False).all()
        context.update({'info_fields': self.info_fields, 'moditems': modItems, 'id': pk})
        return context


class ModifierGroupDeleteView(MessageDeleteView):
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.archived = True
        modifiers = self.object.modifiers.all()
        for modifiers in modifiers:
            modifiers.archived = True
            modifiers.save()
        self.object.modifiers.remove(self.kwargs['pk'])
        self.object.save()
        return HttpResponseRedirect(success_url)


class ModifierGroupCrud(ExtendModelCrud):
    update_class_view = ModifierGroupUpdateView
    list_class_view = ModifierGroupListView
    detail_class_view = ModifierGroupDetailView
    delete_class_view = ModifierGroupDeleteView


modifier_group_crud = ModifierGroupCrud(
    model=products_models.ModifierGroup,
    fields=('name', 'select_multiple'),
    info_fields=('id', 'name', 'select_multiple')
)


class ModifierListView(LoginReqListView):
    form_model = ModifierForm

    def get_context_data(self, **kwargs):
        return {'object_list': self.get_queryset(), 'form': self.form_model}


class ModifierUpdateView(MessageUpdateView):
    form_class = ModifierForm

    def get_success_url(self):

        return reverse('modifiergroup_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.is_ajax():
            if request.POST.get('name') == 'active':
                value = False
                if request.POST.get('value') == 'True':
                    value = True
                self.object.active = value
            elif request.POST.get('name') == 'group':
                for id in dict(request.POST)['value[]']:
                    self.object.group.clear()
                    self.object.group.add(products_models.ModifierGroup.objects.get(pk=id))
            else:
                setattr(self.object, request.POST.get('name'), request.POST.get('value'))

            self.object.save()
            return shortcuts.redirect(self.get_success_url())
        return super(MessageUpdateView, self).post(request, *args, **kwargs)


class ModifierCreateView(MessageCreateView):
    form_class = ModifierForm

    def get_success_url(self):
        return reverse('modifiergroup_list')


class ModifierDeleteView(MessageDeleteView):
    def get_success_url(self):
        return reverse('modifiergroup_list')


class ModifierCrud(ExtendModelCrud):
    list_class_view = ModifierListView
    update_class_view = ModifierUpdateView
    create_class_view = ModifierCreateView
    delete_class_view = ModifierDeleteView


modifier_crud = ModifierCrud(
    model=products_models.Modifier,
    info_fields=('name', 'group', 'cost', 'price', 'active')
)


class CategoryUpdateView(MessageUpdateView):
    form_class = CategoryForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.is_ajax():
            if request.POST.get('name') == 'active':
                value = False
                if request.POST.get('value') == 'true':
                    value = True
                self.object.active = value
            elif request.POST.get('name') == 'parent':
                if request.POST.get('value') == '':
                    self.object.parent = None
                else:
                    parent = products_models.Category.objects.get(pk=request.POST.get('value'))
                    self.object.parent = parent
            else:
                setattr(self.object, request.POST.get('name'), request.POST.get('value'))
            self.object.save()
            return shortcuts.redirect(self.get_success_url())
        return super(MessageUpdateView, self).post(request, *args, **kwargs)


class CategoryCreateView(MessageCreateView):
    form_class = CategoryForm


class CategoryListView(LoginReqListView):
    form_class = CategoryForm
    paginate_by = 100

    def get_context_data(self, **kwargs):
        return {
            'object_list': self.get_queryset(),
            'form': self.form_model,
            'form_class': self.form_class()}


class CategoryCrud(ExtendModelCrud):
    list_class_view = CategoryListView
    update_class_view = CategoryUpdateView
    create_class_view = CategoryCreateView


category_crud = CategoryCrud(
    model=products_models.Category,
    info_fields=('name', 'parent', 'color', 'sorting', 'active')
)


class RewardsListView(LoginReqListView):
    form_model = RewardsForm


class RewardsCreateView(MessageCreateView):
    form_class = RewardsForm


class RewardsUpdateView(MessageUpdateView):
    form_class = RewardsForm


class RewardsCrud(ExtendModelCrud):
    list_class_view = RewardsListView
    update_class_view = RewardsUpdateView
    create_class_view = RewardsCreateView


rewards_crud = RewardsCrud(
    model=products_models.Reward,
)

tax_rate_crud = ExtendModelCrud(
    model=products_models.TaxRate,
    fields=('id', 'name', 'rate'),
    info_fields=('name', 'rate')
)

discount_crud = ExtendModelCrud(
    model=products_models.Discount,
    fields=('id', 'name', 'value', 'type'),
    info_fields=('name', 'value', 'type')
)


class CreateEmployeeView(MessageCreateView):
    form_class = EmployeeCreateForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            employees_models.Employee.objects.create_user(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                name=form.cleaned_data['name'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                zipcode=form.cleaned_data['zipcode'],
                phone=form.cleaned_data['phone'],
                pin=form.cleaned_data['pin'],
                hourly_rate=form.cleaned_data['hourly_rate'],
                role=form.cleaned_data['role'],
                address2=form.cleaned_data['address2'],
                store=form.cleaned_data['store'],
                photo=form.cleaned_data['photo']
            )
            return shortcuts.redirect('employee_list')
        else:
            return shortcuts.render(request, 'employee_create.html', {'form': form})


class UpdateEmployeeView(MessageUpdateView):
    form_model = EmployeeForm

    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     self.object.password = hashers.make_password(self.object.password)
    #     self.object.save()
    #     self.set_message()
    #     return shortcuts.redirect(self.get_success_url())

    # def post(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     self.object.password = hashers.make_password(request.POST.get('password'))
    #     # super(MessageUpdateView, self).post(request, *args, **kwargs)
    #     context = self.get_context_data()
    #     # context['filter_tag']=request.POST.get('filter_tag')
    #     return self.render_to_response(context)
    #     # return shortcuts.redirect(self.get_success_url())


class EmployeeListView(LoginReqListView):
    form_model = EmployeeForm

    def get_context_data(self, **kwargs):
        return {'object_list': self.get_queryset(), 'form': self.form_model}


class EmployeeCrud(ExtendModelCrud):
    create_class_view = CreateEmployeeView
    update_class_view = UpdateEmployeeView
    list_class_view = EmployeeListView


employee_crud = EmployeeCrud(
    model=employees_models.Employee,
    fields=(
        'email', 'name', 'photo', 'address', 'address2', 'city', 'state', 'zipcode', 'phone',
        'pin', 'role', 'hourly_rate'
    ),
    info_fields=(
        'email', 'name', 'photo', 'address', 'address2', 'city', 'state', 'zipcode', 'phone',
        'pin', 'role'
    )
)


class OrderCreateView(MessageCreateView):
    """
    Create view for Order model with initial data, which renders OrderForm.
    Note:
    For this moment it doesn't support post method, because the purpose was to render form with further JS submiting.
    """
    form_class = OrderForm
    initial = {
        "number": '0',
        "subtotal": .0,
        "tax_total": .0,
        "discount_total": .0,
        "grand_total": .0,
        "status": 1,
        "balance_remaining": .0,
    }
    success_url = reverse_lazy('order-list')

    def get(self, request, *args, **kwargs):
        self.user = request.user
        self.initial['emp_open_id'] = self.user.id if self.user else 0
        self.initial['open_date'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        return super(OrderCreateView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['user_id'] = self.user.id
        kwargs['modifier_form'] = OrderModifierForm()
        return super(OrderCreateView, self).get_context_data(**kwargs)


class OrderUpdateView(UpdateView):
    model = Order
    form = OrderUpdateForm
    detail_url_name = None
    message_pattern = None
    form_class = OrderForm
    initial = {
        "number": '0',
        "subtotal": .0,
        "tax_total": .0,
        "discount_total": .0,
        "grand_total": .0,
        "status": 1,
        "balance_remaining": .0,
    }
    success_url = reverse_lazy('order-list')

    def __init__(self, detail_url_name=None, template_name=None, message_pattern=None, model=None, fields=None):
        super(OrderUpdateView, self).__init__()
        self.detail_url_name = detail_url_name
        self.template_name = template_name
        self.message_pattern = message_pattern
        self.model = model
        self.fields = fields

    def post(self, request, *args, **kwargs):
        action = self.request.POST.get('action')
        self.object = Order.objects.get(id=kwargs.get('pk'))
        form = self.form(request.POST)
        if action and form.is_valid():
            return getattr(self, action)(request)
        return redirect('/orders/')

    def refund(self, request):
        self.object.status = 5
        employee = Employee.objects.get(id=request.user.id)
        refunded_payment = Payment.objects.create(
                                order=self.object,
                                employee=employee,
                                amount=-self.object.grand_total,
                                change_amount=0,
                                payment_date=timezone.now(),
                                payment_type='Cash',
                                transaction_type=3,
                                processor_response='APPROVAL'
                            )
        self.object.void_ref = refunded_payment.id
        self.object.save()
        return render(request, 'refund_success.html')

    def duplicate(self, request):
        new_order = self.object
        order_items = OrderItem.objects.filter(order_id=self.object.id)
        new_order.pk = None
        new_order.open_date = timezone.now()
        new_order.status = 1
        new_order.save()
        for item in order_items:
            if item.void_status:
                continue
            item.pk = None
            item.order = new_order
            item.save()
        return redirect('/order/%s/edit' % new_order.id)

    def share(self, request):
        order = SharedOrder.objects.create(order=self.object)
        return redirect('/orders/shared/%s/' % order.identifier)

    def cancel(self, request):
        self.object.status = 4
        Payment.objects.filter(order_id=self.object.id).delete()
        self.object.save()
        return redirect('/orders/')

    def edit(self, request):
        return redirect('/order/%s/edit/' % self.object.id)

    def get(self, request, *args, **kwargs):
        self.user = request.user
        self.initial['emp_open_id'] = self.user.id if self.user else 0
        self.initial['open_date'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        return super(OrderUpdateView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['user_id'] = self.user.id
        kwargs['modifier_form'] = OrderModifierForm()
        kwargs['customers'] = Customer.objects.all()
        return super(OrderUpdateView, self).get_context_data(**kwargs)


class OrderCrud(ExtendModelCrud):
    """
    Generalization for joining Order's views.
    """
    create_class_view = OrderCreateView
    update_class_view = OrderUpdateView


order_crud = OrderCrud(
    model=Order,
)


class OrderItemListView(cbv.ListView):
    """
    Custom Django list view, with custom get method.

    At this moment it doesn't support post method.
    """
    form_class = OrderItemForm
    template_name = 'order_items.html'
    object_list = []

    def get_queryset(self, order_id=0):
        """
        Method gets all active OrderItem entities of specified Order.
        :param order_id: int id of Order model.
        :return: Query object, which contains all OrderItems related to specified Order.
        """
        return OrderItem.objects.filter(order=self.get_order(order_id)).filter(void_status=0)

    @staticmethod
    def get_order(order_id):
        """
        Static method for getting specified Order entity by its ID.
        :param order_id: int id of Order model.
        :return: Order instance.
        """
        return Order.objects.filter(id=int(order_id))

    def get(self, request, *args, **kwargs):
        """
        Overridden get method, which initialize OrderItem form-template and fetch all related OrderItem to given Order,
        with further wrapping of them within forms and returning a rendered template with the context.
        :param request: Request object.
        :param args: None
        :param kwargs: Expecting keyword arguments - order, which specifies ID of Order model.
        :return: Response object, with rendered template.
        """
        context = {}
        order = request.GET.get('order', 0)
        if not order:
            return self.render_to_response(context)
        self.object_list = self.get_queryset(order_id=order)
        context['init_form'] = self.form_class(initial={
            'order_id': int(order),
            'price': .0,
            'employee': request.user.id if request.user else 0,
            'cost': .0,
            'tax': .0,
            'discount': .0,
            'quantity': 1,
            'instance_id': None,
            'void_status': 0,
            'created_at':datetime.now(),
        })
        context.setdefault('forms', [])
        for order_item in self.object_list:
            item_form = self.form_class(instance=order_item)
            item_form.modifiers = [modifier for modifier in OrderModifier.objects.filter(item_id=order_item.id, void_status=False)]
            context['forms'].append(item_form)
        return self.render_to_response(context)


class OrderPaymentView(cbv.DetailView):
    """
    Overridden DetailedView which renders empty formset for Payment.
    """
    form_class = OrderPaymentForm
    object = None
    template_name = "order_payment.html"

    def get(self, request, *args, **kwargs):
        order_id = request.GET.get("order", 0)
        if not order_id:
            raise Http404
        context = dict()
        context['form'] = self.form_class(initial={
            "order_id": order_id,
            "employee_id": request.user.id if request.user else 0,
            "amount": 0.0,
            "amount_paid": 0.0,
            "change_amount": 0.0,
            "tips": 0.0,
        })
        context['currency'] = [1, 2, 5, 10, 20, 50, 100]  # Available USD currency.
        return self.render_to_response(context)


class CreateCustomerView(MessageCreateView):
    form_class = AddCustomerForm


class UpdateCustomerView(MessageUpdateView):
    form_class = CustomerForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.is_ajax():

            name = request.POST.get('name', False)
            if name == 'group':
                self.object.group = CustomerGroup.objects.get(pk=request.POST.get('value'))
            else:
                setattr(self.object, request.POST.get('name'), request.POST.get('value'))
            self.object.save()
            # return shortcuts.redirect(self.get_success_url())
            return HttpResponse(json.dumps({'status': '200'}), content_type="application/json")
        else:
            return super(UpdateCustomerView, self).post(request, *args, **kwargs)


class CustomerListView(LoginReqListView):
    form_model = CustomerForm

    def post(self, request, *args, **kwargs):
        search_phrase = request.POST.get('filter_tag')
        qs = super(LoginReqListView, self).get_queryset()
        from django.db.models import Q
        self.object_list = qs.filter(Q(last_name__icontains=search_phrase) | Q(first_name__icontains=search_phrase) | Q(
            email__icontains=search_phrase) | Q(phone__icontains=search_phrase), archived=False)
        context = self.get_context_data()
        context['filter_tag'] = request.POST.get('filter_tag')
        context['form'] = self.form_model
        qs = self.object_list
        self.request.session['result_cqs'] = unicode(qs.query)
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        context['form'] = self.form_model
        qs = self.get_queryset()
        self.request.session['result_cqs'] = unicode(qs.query)
        return self.render_to_response(context)

        # def get_context_data(self,**kwargs):
        #     return {'object_list': self.get_queryset(), 'form': self.form_model}


class CustomerExportCsvView(LoginReqListView):
    def get(self, request, *args, **kwargs):
        raw_query = list(request.session['result_cqs'])
        a = 0
        for i, j in enumerate(raw_query):
            if j == '%' and a == 0:
                raw_query[i] = '"%%'
                a += 1
            elif j == '%' and a == 1:
                raw_query[i] = '%%"'
                a += 1
            elif j == '%' and a == 2:
                raw_query[i] = '"%%'
                a += 1
            elif j == '%' and a == 3:
                raw_query[i] = '%%"'
                a += 1
            elif j == '%' and a == 4:
                raw_query[i] = '"%%'
                a += 1
            elif j == '%' and a == 5:
                raw_query[i] = '%%"'
                a += 1
            elif j == '%' and a == 6:
                raw_query[i] = '"%%'
                a += 1
            elif j == '%' and a == 7:
                raw_query[i] = '%%"'

        y = "".join(raw_query)
        qs = Customer.objects.raw(str(y.encode('utf-8')))

        model = qs.model
        model_fields = model._meta.fields + model._meta.many_to_many
        headers = [field.name for field in model_fields]  # Create CSV headers

        def get_row(obj):
            row = []
            for field in model_fields:
                if type(field) == models.ForeignKey:
                    val = getattr(obj, field.name)
                    if val:
                        val = val.__unicode__()
                elif type(field) == models.ManyToManyField:
                    val = u', '.join([item.__unicode__() for item in getattr(obj, field.name).all()])
                elif field.choices:
                    val = getattr(obj, 'get_%s_display' % field.name)()
                else:
                    val = getattr(obj, field.name)
                row.append(unicode(val).encode("utf-8"))
            return row

        def stream(headers, data):  # Helper function to inject headers
            if headers:
                yield headers
            for obj in data:
                yield get_row(obj)

        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)

        response = StreamingHttpResponse(
            (writer.writerow(row) for row in stream(headers, qs)),
            content_type="text/csv")

        response['Content-Disposition'] = 'attachment; filename="customer.csv"'
        return response


class CustomerCrud(ExtendModelCrud):
    create_class_view = CreateCustomerView
    update_class_view = UpdateCustomerView
    list_class_view = CustomerListView


customer_crud = CustomerCrud(
    model=employees_models.Customer,
    fields=(
        'first_name', 'last_name', 'email', 'phone', 'profile_key', 'address', 'rewards_points',
        'account_number', 'notes'
    ),
    info_fields=(
        'first_name', 'last_name', 'email', 'phone', 'profile_key', 'address', 'rewards_points',
        'account_number', 'notes'
    )
)


class TaskinGroupCreateView(LoginReqListView):
    form_model = CustomerForm


class TaskinGroupCrud(ExtendModelCrud):
    pass


taskin_group_crud = TaskinGroupCrud(
    model=CustomerGroup
)


class TableUpdateView(MessageUpdateView):
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(MessageUpdateView, self).post(request, *args, **kwargs)


class TableCrud(ExtendModelCrud):
    update_class_view = TableUpdateView


table_crud = TableCrud(
    model=products_models.Table,
    fields=(
        'section', 'table_name', 'table_image', 'x_value',
        'y_value', 'number_people'
    ),
    info_fields=(
        'section', 'table_name', 'table_image', 'x_value',
        'y_value', 'number_people', 'current_order'
    )
)


class TableSectionUpdateView(MessageUpdateView):
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.is_ajax():
            if request.POST.get('name') == 'store':
                store = products_models.Store.objects.get(pk=request.POST.get('value'))
                self.object.store = store
            else:
                setattr(self.object, request.POST.get('name'), request.POST.get('value'))
            self.object.save()
            return shortcuts.redirect(self.get_success_url())
        return super(MessageUpdateView, self).post(request, *args, **kwargs)


class TableSectionListView(LoginReqListView):
    form_model = TableSectionForm

    def get_context_data(self, **kwargs):
        return {'object_list': self.get_queryset(), 'form': self.form_model}


class TableSectionCrud(ExtendModelCrud):
    list_class_view = TableSectionListView
    update_class_view = TableSectionUpdateView


tablesection_crud = TableSectionCrud(
    model=products_models.TableSection,
    fields=(
        'section_name', 'store'
    ),
    info_fields=(
        'section_name', 'store'
    )
)


class StoreDetailView(InfoFieldsDetailView):

    def get_context_data(self, **kwargs):

        from django.conf import settings

        context = super(StoreDetailView, self).get_context_data(**kwargs)
        db_name = settings.DATABASES.get('default').get('NAME')
        context['db'] = db_name
        return context


class StoreCrudExtendedModel(ExtendModelCrud):
    detail_class_view = StoreDetailView

store_crud = StoreCrudExtendedModel(
    model=products_models.Store,
    fields=(
        'name', 'logo', 'number', 'address', 'address_2', 'city', 'state',
        'zipcode', 'phone', 'fax', 'email', 'website', 'tax_rate', 'package',
        'xweb_url', 'xweb_terminal_id', 'xweb_id', 'xweb_auth_key', 'xweb_industry', 'timezone'
    ),
    info_fields=(
        'name', 'logo', 'number', 'address', 'address_2', 'city', 'state',
        'zipcode', 'phone', 'fax', 'email', 'website', 'tax_rate', 'package',
        'xweb_url', 'xweb_terminal_id', 'xweb_id', 'xweb_auth_key', 'xweb_industry', 'timezone'
    )
)

terminal_crud = ExtendModelCrud(
    model=products_models.Terminal,
    fields=('name', 'mac_id', 'pole_display', 'mode'),
    info_fields=('name', 'mac_id', 'pole_display', 'mode')

)


class QuickProductAdd(MessageCreateView):
    form_class = QuickAddProductForm
    template_name = 'custom/quickproductadd.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            product = products_models.Product()
            product.tax_status = 1
            product.tax_rate = TaxRate.objects.get(id=1)
            cat = Category.objects.get(id=1)
            product.barcode = form.cleaned_data['barcode']
            product.color = 1
            product.name = form.cleaned_data['name']

            product.price = 0
            if not (form.cleaned_data['price'] is None):
                product.price = form.cleaned_data['price']

            product.stock = 0
            if not (form.cleaned_data['stock'] is None):
                product.stock = form.cleaned_data['stock']

            product.cost = 0
            product.sorting = 0
            product.change_reason = "Product created"
            product.save()
            product.categories.add(cat)

            return shortcuts.redirect('product_list')
        else:
            return shortcuts.render(request, 'product_create.html', {'form': form})


class CsvParserView(cbv.CreateView):
    template_name = 'import_csv.html'
    form_model = CvsUploadForm
    model = products_models.Csv

    def post(self, request, *args, **kwargs):
        if request.FILES.get('file') and request.FILES['file'].content_type == u'text/csv':
            request.FILES['group_csv'] = request.FILES['file']
            form = CvsUploadForm(request.POST, request.FILES)
        else:
            return HttpResponse('Error! Wrong type of file, expected csv',
                                status=status.HTTP_400_BAD_REQUEST)
        if form.is_valid():

            new_group = form.save()
            with open(new_group.group_csv.path, 'rU') as csvfile:
                wszystkie = csv.DictReader(csvfile, delimiter=',')
                try:
                    for w in wszystkie:
                        if w['name'] != '':
                            products = None
                            if w['barcode']:
                                products = products_models.Product.objects.filter(barcode=w['barcode'])
                                is_created = False
                            if not products:
                                products = [products_models.Product(), ]
                                is_created = True
                            for product in products:
                                product.name = w['name']
                                product.image = w['image']
                                product.color = w['color'] == None and int(w['color']) or None
                                product.sorting = w['sorting'] == None and int(w['sorting']) or None
                                product.cost = w['cost'] != '' and float(w['cost']) or 0.0
                                product.price = w['price'] != '' and float(w['price']) or 0.0
                                product.barcode = w['barcode']
                                product.stock = w['stock'] == None and int(w['stock']) or None
                                product.tax_rate_id = int(w['tax_rate'])
                                product.tax_status = int(w['tax_status'])
                                product.active = w['active'] == 'True' and True or False
                                product.archived = w['archived'] == 'True' and True or False
                                product.price_adjust = int(w['price_adjust'])
                                product.print_to = w['print_to'] == 'True' and True or False
                                product.printer_id = w['printer']
                                if is_created:
                                    product.change_reason = "Product updated from CSV"
                                else:
                                    product.change_reason = "Product created from CSV"
                                product.save()

                                categoryies = str(w["categories"]).strip().split(',')
                                for category_str in categoryies:
                                    categories = products_models.Category.objects.filter(name=category_str)
                                    if categories:
                                        product.categories.add(*categories)
                except KeyError:
                    return HttpResponse("Error! Unexpected csv format", status=status.HTTP_400_BAD_REQUEST)
            # unlink(new_group.group_csv.path)
            # new_group.delete()
            return shortcuts.render(request, self.template_name, {'form': self.form_model})
        else:
            print 'form Invalid'
        return shortcuts.render(request, self.template_name, {'form': self.form_model})

    def get_context_data(self, **kwargs):
        return {'object_list': self.get_queryset(), 'form': self.form_model}


class CsvParserCustomer(cbv.CreateView):
    template_name = 'scv_parser_customer.html'
    form_model = CvsCustomerUploadForm
    model = employees_models.CsvCustomer

    def post(self, request, *args, **kwargs):
        form = CvsCustomerUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # if request.POST.get('truncate'):
            #     print 'truncate true'

            new_group = form.save()
            with open(new_group.group_csv.path, 'rU') as csvfile:
                wszystkie = csv.DictReader(csvfile, delimiter=',')
                for w in wszystkie:
                    try:
                        customer = employees_models.Customer()
                        try:
                            customer_group = CustomerGroup.objects.filter(name=w['customer_group'])[0]
                        except IndexError:
                            customer.group_id = None
                        else:
                            customer.group_id = customer_group.id
                        customer.first_name = w['first_name']
                        customer.last_name = w['last_name']
                        customer.email = w['email']
                        customer.phone = w['phone']
                        customer.address = w['address']
                        customer.rewards_points = int(w['rewards_points'])
                        customer.account_number = w['account_number']
                        customer.notes = w['notes']
                        customer.city = w['city']
                        customer.state = w['state']
                        customer.zipcode = w['zipcode']
                        customer.save()
                    except ValueError:
                        raise ValueError('Wrong types passed in scv file')
            return shortcuts.render(request, self.template_name, {'form': self.form_model})
        else:
            print 'form Invalid'
        return shortcuts.render(request, self.template_name, {'form': self.form_model})

    def get_context_data(self, **kwargs):
        return {'object_list': self.get_queryset(), 'form': self.form_model}


class ShowStock(ProductListView):
    template_name = 'product_list_stock.html'
    model = Product
    paginate_by = 20


##################################Supplier#################################################

class CreateSupplierView(MessageCreateView):
    form_class = AddSupplierForm


class UpdateSupplierView(MessageUpdateView):
    form_class = SupplierForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.is_ajax():
            setattr(self.object, request.POST.get('name'), request.POST.get('value'))
            self.object.save()
            return HttpResponse(json.dumps({'status': '200'}), content_type="application/json")
        else:
            return super(UpdateSupplierView, self).post(request, *args, **kwargs)


class SupplierListView(LoginReqListView):
    form_model = SupplierForm

    def post(self, request, *args, **kwargs):
        search_phrase = request.POST.get('filter_tag')
        qs = super(LoginReqListView, self).get_queryset()
        from django.db.models import Q
        self.object_list = qs.filter(Q(last_name__icontains=search_phrase) | Q(first_name__icontains=search_phrase) | Q(
            email__icontains=search_phrase) | Q(phone__icontains=search_phrase), archived=False)
        context = self.get_context_data()
        context['filter_tag'] = request.POST.get('filter_tag')
        context['form'] = self.form_model
        qs = self.object_list
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        context['form'] = self.form_model
        qs = self.get_queryset()
        return self.render_to_response(context)


class SupplierCrud(ExtendModelCrud):
    create_class_view = CreateSupplierView
    update_class_view = UpdateSupplierView
    list_class_view = SupplierListView


supplier_crud = SupplierCrud(
    model=employees_models.Supplier,
    fields=(
        'id', 'supplier', 'default_markup', 'description', 'company', 'first_name', 'last_name', 'phone',
        'mobile', 'fax', 'email', 'website', 'street', 'suburb', 'city', 'postcode', 'state', 'country'
    ),
    info_fields=(
        'id', 'supplier', 'default_markup', 'description', 'company', 'first_name', 'last_name', 'phone',
        'mobile', 'fax', 'email', 'website', 'street', 'suburb', 'city', 'postcode', 'state', 'country'
    )
)
