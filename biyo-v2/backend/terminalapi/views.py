import  logging
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from django.db.models import F, Sum
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from reports.views import BaseProductForReportsView
from taskin.models import *
from terminalapi.forms import PasswordProtectionForClearSales
from terminalapi.models import ProjectVersion
from terminalapi.serializers import *


# TODO: NEED TOTAL REFACTORING THIS "CODE"!!!


DLVRAPP_SIGN = "Created with Order Delivery app."

logger = logging.getLogger('TerminalAPI_v2')


def is_delivery_order_app(obj):
    if isinstance(obj, Order):
        return obj.description == DLVRAPP_SIGN
    elif isinstance(obj, OrderItem):
        return obj.order.description == DLVRAPP_SIGN
    elif isinstance(obj, OrderModifier):
        return obj.item.order.description == DLVRAPP_SIGN
    return False


def change_order_by_item(item):
    old_price, old_tax, old_discount, old_quantity = 0, 0, 0, 0
    tax = 0
    if item.product.tax_status == 0:
        # taxable
        item.tax = item.product.tax_rate.rate / 100
        logger.info(item.tax)
    else:
        # not taxable
        item.tax = 0
        logger.info(item.tax)
    if item.id:
        old_item = OrderItem.objects.get(pk=item.id)
        old_price = old_item.price
        old_discount = old_item.discount
        old_quantity = old_item.quantity
        old_tax = old_item.tax * old_quantity
    item_price = item.price
    item_discount = item.discount
    item_qty = item.quantity
    if item.void_status:
        item_qty = 0
    special_price = SpecialPrices.objects.filter(archived=False,
                                                 group__archived=False,
                                                 product=item.product,
                                                 group__taskin_group=item.order.customer,
                                                 ).first()
    if special_price:
        item_price = special_price.price
        item.price = item_price
    item_tax = item.tax * item_qty
    item_cost = (item_price - item_discount) * item_qty
    old_cost = (old_price - old_discount) * old_quantity
    modifiers_diff = 0
    if old_quantity != item_qty:
        qdiff = item_qty - old_quantity
        modifiers_diff = item.get_modifiers().aggregate(sum=Sum('price'))['sum'] or 0
        modifiers_diff = modifiers_diff * qdiff
    # making one-query-update to avoid race conditions
    if not item.void_status or item.id:
        item.order._meta.model.objects.filter(id=item.order_id).update(
            subtotal=F('subtotal') - old_cost + item_cost + modifiers_diff,
            tax_total=F('tax_total') - old_tax + item_tax,
            discount_total=F('discount_total') - old_discount * old_quantity + item_discount * item_qty,
            grand_total=F('grand_total') - old_tax - old_cost + item_tax + item_cost + modifiers_diff,
            balance_remaining=F('balance_remaining') - old_tax - old_cost + item_tax + item_cost + modifiers_diff,
        )


def change_order_by_modifier(modifier):
    old_price = 0
    if modifier.id:
        old_modifier = OrderModifier.objects.get(pk=modifier.id)
        old_price = old_modifier.price
    mdf_cost = modifier.price * modifier.item.quantity
    if modifier.void_status:
        mdf_cost = 0
    old_cost = old_price * modifier.item.quantity
    # making one-query-update to avoid race conditions
    if not modifier.void_status or modifier.id:
        modifier.item.order._meta.model.objects.filter(id=modifier.item.order_id).update(
            subtotal=F('subtotal') - old_cost + mdf_cost,
            grand_total=F('grand_total') - old_cost + mdf_cost,
            balance_remaining=F('balance_remaining') - old_cost + mdf_cost,
        )


def get_serialized_page(request, query, serializer_class, size=20):
    paginator = Paginator(query, size)
    page = request.QUERY_PARAMS.get('page') or 1
    try:
        objs = paginator.page(page)
    except PageNotAnInteger:
        objs = paginator.page(1)
    except EmptyPage:
        objs = paginator.page(paginator.num_pages)
    serializer_context = {'request': request}
    serializer = serializer_class(objs, context=serializer_context)
    logger.info(serializer_context, request.DATA)
    return serializer


def get_sync_view(klass, serializer_class):
    @api_view(['GET'])
    def sync_method(request):
        get_params = request.GET.copy()
        page_size = 50
        if klass == CustomerGroup:
            page_size = 1000
        klass_fields = klass._meta.get_all_field_names()
        filter_args = {}
        if 'archived' in klass_fields:
            filter_args['archived'] = False
        order_by = get_params.get('order_by', '')
        if order_by not in klass_fields:
            token = order_by.split('__')[0]
            token = token[1:] if len(token) and token[0] == '-' else token
            if not any(token in x for x in klass_fields) or not len(token):
                order_by = 'id'

        filter_args.update({key: get_params.get(key) for key in get_params.keys() if key in klass_fields})
        logger.info(filter_args)

        page = get_serialized_page(request, klass.objects.filter(**filter_args).order_by(order_by),
                                   serializer_class, size=page_size)
        logger.info(page)
        logger.info(request.DATA)
        return Response(data=page.data)

    return sync_method


def get_add_view(add_serializer_class, serializer_class):
    @api_view(['POST'])
    def add_method(request):
        # monkeypatching - start
        req_data = request.DATA
        # replace 'customer_id' with 'customer' in data. Clients use different format
        # and we'd better handle it here instead of dealing with them
        # (terminal app sends it as 'customer_id' while others as 'customer' and it is expected in serializers)
        # TODO: fixed in terminal newer than build 'v0.1-466' (Mar 31 2016).
        # Probably would be safe to delete after July-Sep 2016 (see below the same patches too)
        if 'customer_id' in req_data:
            req_data['customer'] = req_data['customer_id']
            del req_data['customer_id']
        if req_data.get('customer') in ['0', 0]:
            req_data['customer'] = None
        # monkeypatching - end
        serializer = add_serializer_class(data=req_data)
        if serializer.is_valid():

            if type(serializer) == AddOrderSerializer:
                if is_delivery_order_app(serializer.object):
                    # set all to 0 and add values when save items
                    serializer.object.subtotal = 0
                    serializer.object.tax_total = 0
                    serializer.object.discount_total = 0
                    serializer.object.grand_total = 0
                    serializer.object.balance_remaining = 0

            elif type(serializer) == AddOrderModifierSerializer:
                if is_delivery_order_app(serializer.object):
                    change_order_by_modifier(serializer.object)
            elif type(serializer) == AddOrderItemSerializer:
                order_status = int(serializer.object.order.status)
                if order_status == 3 and serializer.object.void_status != 1:
                    # TODO: here to rewrite deducting with using 'objects.update()', but don't break history!
                    serializer.object.product.stock -= serializer.object.quantity
                    serializer.object.product.change_reason = "Order #%s" % (serializer.object.order.id)
                    serializer.object.product.save()

                # try:
                #     serializer.object.product.stock -= serializer.object.quantity
                #     serializer.object.product.save()
                # except:
                #     pass
                # # TODO: if product doesn't exists
                if serializer.object.product is None:

                    product = Product.objects.filter(name=serializer.object.name, price=serializer.object.price).all()
                    if product:
                        for product in product[:1]:
                            serializer.object.product = product
                    else:
                        product = Product.objects.filter(name=serializer.object.name).all()
                        if product:
                            for product in product[:1]:
                                serializer.object.product = product
                        else:
                            serializer.object.product = None
                            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                # change order's values
                if is_delivery_order_app(serializer.object):
                    change_order_by_item(serializer.object)

                # if serializer.object.order.description == "Created with Order Delivery app.":
                #     # looking for special price for this product
                #     # ONLY applicable for order delvery app
                #     special_price = SpecialPrices.objects.filter(archived=False,
                #                                                  group__archived=False,
                #                                                  product=serializer.object.product,
                #                                                  group__taskin_group=serializer.object.order.customer,
                #                                                  ).first()
                #     if special_price:
                #         # reduce the price for order_item and recalculate subtotal for order
                #         tax = 0
                #         if serializer.object.product.tax_status == 0:
                #             # taxable
                #             tax = serializer.object.product.tax_rate.rate / 100
                #             serializer.object.tax = serializer.object.product.tax_rate.rate / 100
                #         else:
                #             # not taxable
                #             serializer.object.tax = 0
                #         price_diff = serializer.object.product.price - special_price.price
                #         cost_diff = price_diff * serializer.object.quantity
                #         tax_diff = price_diff * serializer.object.quantity * tax
                #         serializer.object.price = special_price.price
                #         # making one-query-update to avoid race conditions
                #         order = serializer.object.order
                #         order._meta.model.objects.filter(id=order.id).update(
                #             subtotal=F('subtotal') - cost_diff,
                #             tax_total=F('tax_total') - tax_diff,
                #             grand_total=F('grand_total') - tax_diff - cost_diff,
                #             balance_remaining=F('balance_remaining') - tax_diff - cost_diff,
                #         )

            obj = serializer.save()

            data = serializer_class(obj).data
            if "frontend_id" in req_data:
                data["frontend_id"] = req_data.get("frontend_id")
            data["db_table"] = obj._meta.db_table
            logger.info(req_data)
            logger.info(data)
            logger.info(request.DATA)
            return Response(data=data, status=status.HTTP_201_CREATED)
        else:
            logger.info(request.DATA)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return add_method


def get_update_view(klass, serializer_class):
    @api_view(['PUT'])
    def update_method(request, pk):
        # monkeypatching - start (see explanation above)
        req_data = request.DATA
        # TODO: fix in clients
        logger.info(req_data)
        if 'customer_id' in req_data:
            req_data['customer'] = req_data['customer_id']
            del req_data['customer_id']
        if req_data.get('customer') in ['0', 0]:
            req_data['customer'] = None
        # monkeypatching - end
        try:
            obj = klass.objects.get(pk=pk)
        except klass.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = serializer_class(obj, data=req_data, partial=True)
        if serializer.is_valid():
            if is_delivery_order_app(serializer.object):
                if klass == OrderItem:
                    change_order_by_item(serializer.object)
                elif klass == OrderModifier:
                    change_order_by_modifier(serializer.object)
            obj = serializer.save()
            logger.info(obj)
            data = serializer_class(obj).data
            if "frontend_id" in req_data:
                data["frontend_id"] = req_data.get("frontend_id")
            data["db_table"] = obj._meta.db_table
            logger.info(data)
            logger.info(request.DATA)
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            logger.info(request.DATA)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    logger.info(update_method)
    return update_method

    # 1 - 'Open', 2 - hold


product_open_status = (1, 2)
# 3 - closed
product_close_status = (3,)
# 5- refunded
product_refunded_status = (5,)


@api_view(['PUT'])
def update_order(request, pk):
    # monkeypatching - start (see explanation above)
    req_data = request.DATA
    # TODO: fix in clients
    if 'customer_id' in req_data:
        req_data['customer'] = req_data['customer_id']
        del req_data['customer_id']
    if req_data.get('customer') in ['0', 0]:
            req_data['customer'] = None
    # monkeypatching - end
    try:
        obj_order = Order.objects.get(pk=pk)
        order_status = int(obj_order.status)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    obj_data = req_data
    if is_delivery_order_app(obj_order):
        # don't allow to change these fields directly
        for k in ('subtotal', 'tax_total', 'discount_total', 'grand_total', 'balance_remaining'):
            if k in obj_data:
                del obj_data[k]

    serializer = OrderSerializer(obj_order, data=obj_data, partial=True)
    if serializer.is_valid():
        new_order_status = int(serializer.object.status)
        if order_status != new_order_status:
            items = serializer.object.items.exclude(void_status=True).all()
            for item in items:
                old_stock = item.product.stock
                if (order_status == 1 or order_status == 2) and new_order_status == 3:
                    item.product.stock = (item.product.stock or 0) - item.quantity
                if order_status == 3 and new_order_status == 5:
                    item.product.stock += item.quantity
                if old_stock != item.product.stock:
                    item.product.change_reason = "Order #%s" % (pk)
                    item.product.save()
        obj = serializer.save()
        data = OrderSerializer(obj).data
        if "frontend_id" in req_data:
            data["frontend_id"] = req_data.get("frontend_id")
        data["db_table"] = obj._meta.db_table
        logger.info(request.DATA)
        logger.info(req_data)
        return Response(data=data, status=status.HTTP_200_OK)
    else:
        logger.info(request.DATA)
        logger.info(req_data)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


sync_employees = get_sync_view(Employee, PaginatedEmployeeSerializer)
sync_customers = get_sync_view(Customer, PaginatedCustomerSerializer)
sync_suppliers = get_sync_view(Supplier, PaginatedSupplierSerializer)
sync_orders = get_sync_view(Order, PaginatedOrderSerializer)
sync_orders_items = get_sync_view(OrderItem, PaginatedOrderItemsSerializer)
sync_orders_modifiers = get_sync_view(OrderModifier, PaginatedOrderModifierSerializer)
sync_orders_options = get_sync_view(OrderOption, PaginatedOrderOptionSerializer)
sync_payments = get_sync_view(Payment, PaginatedPaymentSerializer)
sync_products = get_sync_view(Product, PaginatedProductSerializer)
sync_products_id_name = get_sync_view(Product, ProductIdNameSerializer)
sync_taxrate = get_sync_view(TaxRate, PaginatedTaxRateSerializer)
sync_categories = get_sync_view(Category, PaginatedCategorySerializer)
sync_modifiers_groups = get_sync_view(ModifierGroup, PaginatedModifierGroupSerializer)
sync_modifiers = get_sync_view(Modifier, PaginatedModifierSerializer)
sync_discount = get_sync_view(Discount, PaginatedDiscountSerializer)
sync_store = get_sync_view(Store, PaginateStoreSerializer)
sync_table = get_sync_view(Table, PaginateTableSerializer)
sync_tablesection = get_sync_view(TableSection, PaginateTableSectionSerializer)
sync_terminal = get_sync_view(Terminal, PaginateTerminalSerializer)
sync_prod2mg = get_sync_view(Product.modifier_groups.through, PaginateProg2MgSerializer)
sync_prod2cat = get_sync_view(Product.categories.through, PaginatedProg2CatSerializer)
sync_shifts = get_sync_view(Shift, PaginatedShiftSerializer)
sync_payouts = get_sync_view(Payout, PaginatedPayoutSerializer)

sync_taskingroups = get_sync_view(CustomerGroup, PaginatedTaskinGroupSerializer)

sync_printer = get_sync_view(Printer, PaginatedPrinterSerializer)
timeclock = get_sync_view(TimeClock, PaginatedTimeClockSerializer)
rewardcampaigns = get_sync_view(Reward, PaginatedRewardSerializer)

add_order = get_add_view(AddOrderSerializer, OrderSerializer)
add_order_item = get_add_view(AddOrderItemSerializer, OrderItemSerializer)
add_order_item_modifier = get_add_view(AddOrderModifierSerializer, OrderModifierSerializer)
add_customer = get_add_view(CustomerSerializer, CustomerSerializer)
add_employee = get_add_view(EmployeeCreatorSerializer, EmployeeCreatorSerializer)
add_tax = get_add_view(TaxRateSerializer, TaxRateSerializer)
add_store = get_add_view(StoreCreatorAPISerializer, StoreCreatorAPISerializer)
add_product = get_add_view(ProductSerializer, ProductSerializer)
add_printer = get_add_view(AddPrinterSerializer, PrinterSerializer)

add_shift = get_add_view(AddShiftSerializer, ShiftSerializer)
add_payout = get_add_view(AddPayoutSerializer, PayoutSerializer)

# update_order = get_update_view(Order, OrderSerializer)

update_table = get_update_view(Table, TableSerializer)
update_payment = get_update_view(Payment, PaymentSerializer)

update_printer = get_update_view(Printer, PrinterSerializer)

update_employee = get_update_view(Employee, SyncEmployeeSerializer)
update_order_item = get_update_view(OrderItem, OrderItemSerializer)
update_order_item_modifier = get_update_view(OrderModifier, OrderModifierSerializer)

update_shift = get_update_view(Shift, ShiftSerializer)
update_payout = get_update_view(Payout, PayoutSerializer)


@api_view(["GET"])
def sync_products_advanced(request):
    """
    API with nested modifiers groups, modifiers and special prices for each customer group.
    :param request:
    :return:
    """
    data = []
    q = Product.objects.all().select_related("modifier_groups").prefetch_related("modifier_groups__modifiers") \
        .select_related("special_prices_items").prefetch_related("special_prices_items__group").prefetch_related(
            "special_prices_items__group__taskin_group"
    )
    for product in q:
        serialized_p = ProductSerializer(instance=product)
        serialized_p = serialized_p.data
        m_groups = []
        for m_group in product.modifier_groups.all():
            serialized_mg = ModifierGroupSerializer(instance=m_group)
            serialized_mg = serialized_mg.data
            modifiers = []
            for modifier in m_group.modifiers.all():
                serialized_m = ModifierSerializer(instance=modifier)
                modifiers.append(serialized_m.data)
            serialized_mg['modifiers'] = modifiers
            m_groups.append(serialized_mg)
        serialized_p['modifier_groups'] = m_groups
        serialized_p['special_prices'] = [
            {
                'price': special_price.price,
                'group': {'id': special_price.group.id, 'name': special_price.group.name, 'customers': [
                    x.id for x in special_price.group.taskin_group.all()
                ]},
            } for special_price in product.special_prices_items.all()
        ]
        data.append(serialized_p)
        logger.info(data)
        logger.info(request.DATA)
    return Response(data={"results": data, "count": q.count(), "db_table": Product._meta.db_table})


@api_view(["GET"])
def show_special_prices(request):
    """
    Endpoint to see special prices
    """
    queryset = SpecialPrices.objects.all()
    data = map(lambda item: {'id': item.id, 'product_id': item.product_id,
                             'group_id': item.group_id, 'price': item.price}, list(queryset))
    logger.info(queryset)
    logger.info(data)
    logger.info(request.DATA)
    return Response(data={"results": data, "count": queryset.count(), 'db_table': SpecialPrices._meta.db_table})


@api_view(['POST'])
def update_customer(request, pk):
    """
    Updates customer by profile key.

    request: {'profile_key'}

    returns if profile was updated
    {
        'status': 'updated',
        'data': 'cutomer'
    }
    else if cutomer doesn't exists
    {
        'status': 'Not exists'
    }
    """
    try:
        customer = Customer.objects.get(pk=pk)
    except Customer.DoesNotExist:
        return Response({'status': 'Not exists'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CustomerSerializer(customer, request.DATA, partial=True)
    if serializer.is_valid():
        serializer.save()
    logger.info(request.DATA)
    return Response({'status': 'updated', 'data': serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
def update_box_coords(request, pk):
    """
    Updates Box by PK.
    Fields which can be updated:
    'id', 'size_x', 'size_y', 'row', 'col'
    """
    box = Box.objects.get(pk=pk)

    serializer = BoxSerializer(box, request.DATA, partial=True)
    if serializer.is_valid():
        serializer.save()
    logger.info(box)
    logger.info(request.DATA)
    return Response({'status': 'updated'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def update_spicialprices(request, pk):
    """
    Updates special prices for Customer Group
    updates by primary product key
    input :values : group_*
    :return status: 'updates'
    """

    product = Product.objects.get(pk=pk)

    # SpecialPrices

    post = request.POST
    for valname in post:

        val = request.POST[valname]
        groups = valname.split("_")
        modelGroup = CustomerGroup.objects.get(pk=groups[1])
        # print groups[1] + " >>> "  + val
        if val != '':
            try:
                sprice = SpecialPrices.objects.get(product=product, group=modelGroup)
                sprice.price = val
                sprice.save()
            except SpecialPrices.DoesNotExist:
                SpecialPrices.objects.create(product=product, group=modelGroup, price=val)
        elif val == "" or val == 0:
            try:
                sprice = SpecialPrices.objects.get(product=product, group=modelGroup)
                sprice.delete()
            except SpecialPrices.DoesNotExist:
                pass
    logger.info(request.DATA)
    return Response({'status': 'updated'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def check_terminal_mac_id(request):
    if Terminal.objects.filter(mac_id__in=[request.DATA['mac_id'], '*']).exists():
        logger.info(request.DATA)
        return Response({'status': 'allowed'}, status=status.HTTP_200_OK)
    else:
        logger.info(request.DATA)
        return Response({'status': 'Not allowed'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def check_product_barcode(request):
    try:
        product = Product.objects.get(barcode=request.POST.get('barcode'))
        logger.info(request.DATA)
        return Response({'status': 'exists'}, status=status.HTTP_200_OK)
    except Product.DoesNotExist:
        logger.info(request.DATA)
        return Response({'status': 'allowed'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def check_product_barcode_extended(request):
    try:
        if request.POST.get('barcode') == '':
            logger.info(request.DATA)
            return Response({'status': 'allowed'}, status=status.HTTP_200_OK)
        product = Product.objects.get(barcode=request.POST.get('barcode'))
        url = reverse('product_detail', kwargs={'pk': product.id})
        logger.info(product)
        logger.info(url)
        logger.info(request.DATA)
        return Response({'status': 'exists', 'product': {"name": product.name, "url": url}}, status=status.HTTP_200_OK)
    except Product.DoesNotExist:
        logger.info(request.DATA)
        return Response({'status': 'allowed'}, status=status.HTTP_200_OK)


class ClearSales(TemplateView):
    template_name = 'clearorders.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if context["form"].is_valid():
            Order.objects.all().delete()
            Shift.objects.all().delete()
            Payout.objects.all().delete()
            from django.db import connection
            cursor = connection.cursor()
            cursor.execute("ALTER TABLE order_order AUTO_INCREMENT = 1")
            cursor.execute("ALTER TABLE order_orderoption AUTO_INCREMENT = 1")
            cursor.execute("ALTER TABLE order_orderitem AUTO_INCREMENT = 1")
            cursor.execute("ALTER TABLE order_ordermodifier AUTO_INCREMENT = 1")
            cursor.execute("ALTER TABLE payments_shift AUTO_INCREMENT = 1")
            cursor.execute("ALTER TABLE payments_payout AUTO_INCREMENT = 1")
        logger.info(cursor)
        logger.info(request.DATA)
        return super(TemplateView, self).render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(ClearSales, self).get_context_data(**kwargs)
        form = PasswordProtectionForClearSales(self.request.POST or None)  # instance= None
        context["form"] = form
        logger.info(context)
        return context


@api_view(['GET'])
def check_version(request):
    app = ProjectVersion.objects.get(pk=1)
    logger.info(app)
    logger.info(request.DATA)
    return Response(data={'version': app.version, 'link': app.installer.url, 'password': app.password})


@api_view(['POST'])
def add_timeclock_entry(request):
    """
    request: {'employee_id': 1}

    returns if time entry is not closed
    {
        'status': 'updated'
    }
    else
    {
        'status': 'created'
    }
    """
    import datetime
    try:
        employee = Employee.objects.get(pk=request.DATA.get('employee_id'))
    except Employee.DoesNotExist:
        logger.info(request.DATA)
        return Response({'status': 'Not exists'}, status=status.HTTP_404_NOT_FOUND)
    today_range = (datetime.date.today(), datetime.date.today() + datetime.timedelta(days=1))
    i = TimeClock.objects.filter(time_in__range=today_range, time_out=None, employee=employee)
    if i:
        i[0].time_out = datetime.datetime.now()
        i[0].save()
        logger.info(request.DATA)
        return Response({'status': "updated"})
    else:
        TimeClock.objects.create(employee=employee, time_in=datetime.datetime.now())
        logger.info(request.DATA)
        return Response({'status': "created"})


@api_view(['POST'])
def check_owner(request):
    try:
        employee = Employee.objects.get(email=request.DATA.get('email'))
        if hashers.check_password(request.DATA.get('password'), employee.password) and employee.role == 1:
            return Response({'status': 'Allowed'}, status=status.HTTP_200_OK)
        logger.info(request.DATA)
        return Response({'status': 'Not allowed'}, status=status.HTTP_403_FORBIDDEN)
    except Employee.DoesNotExist:
        logger.info(request.DATA)
        return Response({'status': 'Not exists'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def get_detailed_orders(request):
    qs = Order.objects.filter(status=request.DATA.get('status')).order_by('-open_date')
    serializer = get_serialized_page(request, qs, PaginateDetailedOrderSerializer, 8)
    logger.info(request.DATA)
    return Response(data=serializer.data)


@api_view(['GET'])
def get_detailed_order(request, pk):
    order = Order.objects.get(pk=pk)
    serializer = DetailedOrderSerializer(order)
    logger.info(order)
    logger.info(request.DATA)
    return Response(data=serializer.data)


@api_view(['GET'])
def get_customer_balance(request, pk):
    orders = Order.objects.filter(customer=pk)
    remaining_balance = orders.exclude(status__in=[3, 4]).\
        exclude(balance_remaining=None).aggregate(remaining=Sum('balance_remaining'))['remaining'] or 0
    all_order_total = orders.aggregate(total=Sum('grand_total'))['total'] or 0
    logger.info(orders)
    logger.info(request.DATA)
    return Response(data={'remaining_balance': remaining_balance, 'all_orders_total': all_order_total})


@api_view(['GET'])
def get_detailed_tables(request):
    qs = Table.objects.all().order_by('section')
    serializer = get_serialized_page(request, qs, PaginateDetailedTableSerializer, 8)
    logger.info(qs)
    logger.info(request.DATA)
    return Response(data=serializer.data)


@api_view(['POST'])
def set_display_box_element(request, pk):
    box = get_object_or_404(Box, pk=pk)
    element = box.element
    element.type = request.DATA.get('type')
    element.value = request.DATA.get('value')
    box.background_color = request.DATA.get('background_color')
    element.save()
    box.save()
    logger.info(element)
    logger.info(box)
    logger.info(request.DATA)
    return Response()


@api_view(['GET'])
def get_timeclock_id(request, pk):
    timeclock = get_object_or_404(TimeClock, pk=pk)
    serializer = TimeClockSerializer(timeclock)
    logger.info(timeclock)
    logger.info(serializer)
    logger.info(request.DATA)
    return Response(data=serializer.data)


@api_view(['GET'])
def get_product_id_name(request):
    products = Product.objects.all()
    serializer = ProductIdNameSerializer(products)
    logger.info(products)
    logger.info(serializer)
    logger.info(request.DATA)
    return Response(data=serializer.data)


@api_view(['GET'])
def get_display_box_element(request, pk):
    box = get_object_or_404(Box, pk=pk)
    element = box.element
    logger.info(box)
    logger.info(element)
    logger.info(request.DATA)
    return Response(data={'type': element.type, 'value': element.value, 'color': box.background_color})


@api_view(['GET'])
def get_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    serializer = EmployeeSerializer(employee)
    logger.info(employee)
    logger.info(Response(data=serializer.data))
    return Response(data=serializer.data)


@api_view(['GET'])
def get_cats(request):
    try:
        ids = str(request.GET.get('code')).split(',')
    except ValueError:
        pass
    categories = Category.objects.filter(id__in=ids)
    serializer = CategoryQuickChangeSerializer(categories)
    logger.info(categories)
    logger.info(request.DATA)
    return Response(data=serializer.data)


@api_view(['POST'])
def updateProductCategory(request):
    product = Product.objects.get(id=request.POST.get('pk'))
    catpost = request.POST.get('category')
    catids = catpost.split(";")
    product.categories = catids
    product.change_reason = "Update product category"
    product.save()
    logger.info(product)
    logger.info(request.DATA)
    return Response(data='OK')


@api_view(['POST'])
def updateModifiers(request):
    mods = Modifier.objects.get(id=request.POST.get('pk'))
    groups = request.POST.get('groups')
    groupsds = groups.split(";")
    mods.group = (groupsds)
    mods.save()
    logger.info(mods)
    logger.info(request.DATA)
    return Response(data='OK')


@api_view(['GET'])
def get_cat_list(request):
    categories = Category.objects.all()
    serializer = CategoryQuickChangeSerializer(categories)
    logger.info(categories)
    logger.info(request.DATA)
    return Response(data=serializer.data)


@api_view(['GET'])
def get_modifier_group_list(request):
    modifier_groups = ModifierGroup.objects.exclude(archived=True).all()
    serializer = CategoryQuickChangeSerializer(modifier_groups)
    logger.info(modifier_groups)
    logger.info(request.DATA)
    return Response(data=serializer.data)


@api_view(['GET'])
def remove_display_box_element(request, pk):
    """
    This function updates box and elements
    sets up archived = true
    """
    try:
        box = get_object_or_404(Box, pk=pk)
    except Exception:
        return Response(data="Not found")
    element = box.element
    element.archived = True
    box.archived = True
    element.save()
    box.save()
    logger.info(element)
    logger.info(box)
    logger.info(request.DATA)
    return Response(data="Removed")


@api_view(['GET'])
def run_tests(request):
    import unittest
    from tests import OrdersTests
    suite = unittest.TestLoader().loadTestsFromTestCase(OrdersTests)
    temp = unittest.TextTestRunner(verbosity=2).run(suite)
    if temp.wasSuccessful():
        logger.info(request.DATA)
        return Response(data={'output': 'OK, Ran %d tests' % temp.testsRun})
    else:
        failures = []
        for test, err in temp.failures:
            failures.append((str(test), err))
        logger.info(failures)
        logger.info(request.DATA)
        return Response(data={'output': {'failures': failures}})


@api_view(['POST'])
def add_payment(request):
    serializer = AddPaymentSerializer(data=request.DATA)

    filter = {}

    fields = ("payment_date", "employee_id", "batch_num", "amount_paid", "payment_form",
              "change_amount", "transaction_type", "order_id", "amount", "processor_response",
              "payment_type", "approval_code", "signature", "terminal_id", "void_ref", "transaction_id",
              'check_number')

    for field in fields:
        if field != "frontend_id":
            filter[field] = request.DATA.get(field)
    result = Payment.objects.filter(**filter).all()
    if result.count() == 0:
        if serializer.is_valid():
            obj = serializer.save()
            data = PaymentSerializer(obj).data
            if "frontend_id" in request.DATA:
                data["frontend_id"] = request.DATA.get("frontend_id")
            data["db_table"] = obj._meta.db_table
            logger.info(request.DATA)
            logger.info(data)
            return Response(data=data, status=status.HTTP_201_CREATED)
        else:
            logger.info(request.DATA)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        data = PaymentSerializer(result[0]).data
        data["db_table"] = "payments_payment"
        logger.info(request.DATA)
        logger.info(data)
        return Response(data=data, status=status.HTTP_201_CREATED)


class MultipleFieldLookupMixin(object):
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """

    def get_object(self):
        queryset = self.get_queryset()  # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]
        logger.info(queryset)
        return get_object_or_404(queryset, **filter)  # Lookup the object


class RetrieveUserView(MultipleFieldLookupMixin, CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    lookup_fields = ('order',)
    logger.info(queryset)

@api_view(['GET'])
def sales_payments(request):
    from django.db.models import Q
    from django.db.models import Sum
    start, end = BaseProductForReportsView.get_start_end_dates(request)
    shift_info = {}
    employee_info = {}
    try:
        shift_id = int(request.GET.get('shift_id', 0))
    except ValueError:
        shift_id = 0
    if shift_id:
        qs = BaseProductForReportsView.get_orders_with_shift(shift_id=shift_id)
        payments = BaseProductForReportsView.get_payments_with_shift(shift_id=shift_id)
        shift_q = Shift.objects.filter(id=shift_id)
        if shift_q.count():
            instance = Shift.objects.filter(id=shift_id).get()
            employee_info['open'] = EmployeeSerializer(instance=instance.open_shift_employee).data
            if instance.close_shift_employee:
                employee_info['close'] = EmployeeSerializer(instance=instance.close_shift_employee).data
            shift_info = ShiftSerializer(instance=instance).data

    else:
        qs = BaseProductForReportsView.get_orders_with_range(start, end)
        payments = Payment.objects.filter(
            Q(order__open_date__range=(start, end)) | Q(order__close_date__range=(start, end)),
            order__status=3).exclude(order__close_date__gt=end)

    if request.GET.get('terminal'):
        terminal = request.GET.get('terminal')
        payments = payments.filter(Q(terminal_id=terminal))

    if request.GET.get('employee'):
        employee = request.GET.get('employee')
        payments = payments.filter(Q(employee=employee))

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
    # payments end
    logger.info(request.DATA)
    logger.info({
        'sales': {
            'gross_sales': qs.aggregate(sum=Sum('subtotal'))['sum'],
            'discount_total': qs.aggregate(sum=Sum('discount_total'))['sum'],
            'grand_total': qs.aggregate(sum=Sum('grand_total'))['sum'],
            'tax_total': qs.aggregate(sum=Sum('tax_total'))['sum'],
            'tips': qs.aggregate(sum=Sum('payments__tips'))['sum'],
            'active2': 'sales_summary',
        },
        'payments': {
            'refunded': refunded,
            'total_card_sum': total_card_sum,
            'total_before_tips': total_before_tips,
            'tips_sum': tips_sum,
            'other_cc': other_cc,
            'total_sum': total_sum,
            'cash_sum': cash_sum,
            'visa_sum': payments.filter(
                payment_type='Visa'
            ).aggregate(sum=Sum('amount'))['sum'],
            'mastercard_sum': payments.filter(
                payment_type='MasterCard'
            ).aggregate(sum=Sum('amount'))['sum'],
            'american_express_sum': payments.filter(
                payment_type='American Express'
            ).aggregate(sum=Sum('amount'))['sum'],
            'discover_sum': payments.filter(
                payment_type='Discover'
            ).aggregate(sum=Sum('amount'))['sum'],
        },
        'shift': shift_info,
        'open_employee': employee_info.get('open'),
        'close_employee': employee_info.get('close', None),
    })
    return Response(data={
        'sales': {
            'gross_sales': qs.aggregate(sum=Sum('subtotal'))['sum'],
            'discount_total': qs.aggregate(sum=Sum('discount_total'))['sum'],
            'grand_total': qs.aggregate(sum=Sum('grand_total'))['sum'],
            'tax_total': qs.aggregate(sum=Sum('tax_total'))['sum'],
            'tips': qs.aggregate(sum=Sum('payments__tips'))['sum'],
            'active2': 'sales_summary',
        },
        'payments': {
            'refunded': refunded,
            'total_card_sum': total_card_sum,
            'total_before_tips': total_before_tips,
            'tips_sum': tips_sum,
            'other_cc': other_cc,
            'total_sum': total_sum,
            'cash_sum': cash_sum,
            'visa_sum': payments.filter(
                payment_type='Visa'
            ).aggregate(sum=Sum('amount'))['sum'],
            'mastercard_sum': payments.filter(
                payment_type='MasterCard'
            ).aggregate(sum=Sum('amount'))['sum'],
            'american_express_sum': payments.filter(
                payment_type='American Express'
            ).aggregate(sum=Sum('amount'))['sum'],
            'discover_sum': payments.filter(
                payment_type='Discover'
            ).aggregate(sum=Sum('amount'))['sum'],
        },
        'shift': shift_info,
        'open_employee': employee_info.get('open'),
        'close_employee': employee_info.get('close', None),

    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_shift(request, pk):
    """
    API view retrieves Shift instance by ID or raises an exception.
    :param request: HTTPRequest object
    :param pk: int ID of retrieving Shift
    :return: HTTPResponse object or NotFound.
    """
    instance = get_object_or_404(Shift, pk=pk)
    serializer = ShiftSerializer(instance)
    logger.info(instance)
    logger.info(request.DATA)
    return Response(data=serializer.data)


@api_view(['GET'])
def get_payout(request, pk):
    """
    API view retrieves Shift instance by ID or raises an exception.
    :param request: HTTPRequest object
    :param pk: int ID of retrieving Shift
    :return: HTTPResponse object or NotFound.
    """
    instance = get_object_or_404(Payout, pk=pk)
    serializer = PayoutSerializer(instance)
    logger.info(instance)
    logger.info(request.DATA)
    return Response(data=serializer.data)
