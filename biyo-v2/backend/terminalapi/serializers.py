from rest_framework import serializers, pagination
from employees.models import *
# from mobileapi.models import Profile, Transaction, TransactionDetails
# from mobileapi.models import Payment as mobileapi_payment
from order.models import *
from payments.models import *
from products.models import *
from displays.models import *
from taskin.models import CustomerGroup


class PaginationWithDbSerializer(pagination.PaginationSerializer):
    db_table = serializers.SerializerMethodField('get_db_table')

    def get_db_table(self, obj):
        return self.Meta.object_serializer_class.Meta.model._meta.db_table


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = (
            'id', 'name', 'address', 'address2', 'city', 'state', 'zipcode',
            'phone', 'pin', 'role', 'vein_string', 'archived', 'email', 'hourly_rate',
        )


class EmployeeCreatorSerializer(serializers.ModelSerializer):
    store = serializers.PrimaryKeyRelatedField(source='store')

    class Meta:
        model = Employee
        fields = (
            'name', 'password', 'is_staff', 'is_active', 'is_superuser', 'address', 'address2',
            'city', 'state', 'zipcode',
            'phone', 'pin', 'role', 'vein_string', 'archived', 'email', 'hourly_rate', 'store'
        )


class SyncEmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = (
            'id', 'name', 'address', 'address2', 'city', 'state', 'zipcode',
            'phone', 'pin', 'role', 'vein_string', 'archived',
        )


class PaginatedEmployeeSerializer(PaginationWithDbSerializer):

    class Meta:
        object_serializer_class = SyncEmployeeSerializer


class CustomerSerializer(serializers.ModelSerializer):
    account_number = serializers.CharField(required=False)
    customer_group = serializers.PrimaryKeyRelatedField(source='group', required=False)

    class Meta:
        model = Customer
        fields = (
            'account_number', 'id', 'first_name', 'last_name', 'email', 'phone', 'profile_key',
            'address', 'rewards_points', 'notes', 'archived', 'city', 'state', 'zipcode', 'customer_group'
        )


class PaginatedCustomerSerializer(PaginationWithDbSerializer):

    class Meta:
        object_serializer_class = CustomerSerializer


class SupplierSerializer(serializers.ModelSerializer):
    account_number = serializers.CharField(required=False)

    class Meta:
        model = Supplier
        fields = (
            'id', 'supplier', 'default_markup', 'description', 'company', 'first_name', 'last_name', 'phone',
            'mobile', 'fax', 'email', 'website', 'street', 'suburb', 'city', 'postcode', 'state', 'country'
        )


class PaginatedSupplierSerializer(PaginationWithDbSerializer):

    class Meta:
        object_serializer_class = SupplierSerializer


class OrderOptionSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(source='product')

    class Meta:
        model = OrderOption


class PaginatedOrderOptionSerializer(PaginationWithDbSerializer):

    class Meta:
        object_serializer_class = OrderOptionSerializer


class OrderModifierSerializer(serializers.ModelSerializer):
    item_id = serializers.PrimaryKeyRelatedField(source='item')
    group_id = serializers.PrimaryKeyRelatedField(source='group')
    oryginal_id = serializers.PrimaryKeyRelatedField(source='oryginal')

    class Meta:
        model = OrderModifier
        fields = ("id", "item_id", "name", "cost",
                  "price", "oryginal_id", "group_id", "void_status", )


class PaginatedOrderModifierSerializer(PaginationWithDbSerializer):

    class Meta:
        object_serializer_class = OrderModifierSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    order_id = serializers.PrimaryKeyRelatedField(source='order')
    modifiers = OrderModifierSerializer(many=True)

    class Meta:
        model = OrderItem
        fields = ("id", "order_id", "name", "price", "cost", "discount", "tax",
                  "void_status", "employee", "product", "quantity", "modifiers", "terminal_id")


class PaginatedOrderItemsSerializer(PaginationWithDbSerializer):

    class Meta:
        object_serializer_class = OrderItemSerializer


class OrderSerializer(serializers.ModelSerializer):
    emp_open_id = serializers.PrimaryKeyRelatedField(source='emp_open')
    emp_close_id = serializers.PrimaryKeyRelatedField(source='emp_close')
    shift_id = serializers.PrimaryKeyRelatedField(source='shift', required=False)

    class Meta:
        model = Order
        fields = ("id", "number", "subtotal", "tax_total", "discount_total",
                  "grand_total", "balance_remaining", "open_date", "hold_date",
                  "close_date", "status", "description", "emp_open_id",
                  "emp_close_id", "discount_orders", "terminal_id", "customer", 'shift_id')


class PaginatedOrderSerializer(PaginationWithDbSerializer):

    class Meta:
        object_serializer_class = OrderSerializer


class PaymentSerializer(serializers.ModelSerializer):
    order_id = serializers.PrimaryKeyRelatedField(source='order')
    employee_id = serializers.PrimaryKeyRelatedField(source='employee')
    shift_id = serializers.PrimaryKeyRelatedField(source='shift', required=False)

    class Meta:
        model = Payment
        fields = ("id", "order_id", "amount", "amount_paid", "tips", "change_amount", "payment_type",
                  "payment_date", "payment_form", "transaction_type", "batch_num", "approval_code", "transaction_id",
                  "processor_response", "signature", "employee_id", "terminal_id", "void_ref", 'shift_id',
                  'check_number')


class PaginatedPaymentSerializer(PaginationWithDbSerializer):

    class Meta:
        object_serializer_class = PaymentSerializer


class CategoryQuickChangeSerializer(serializers.ModelSerializer):

    def to_native(self, data):
        return {data.id: data.name}

    class Meta:
        model = Category
        fields = ("id", "name")


class CategorySerializer(serializers.ModelSerializer):
    parent_id = serializers.PrimaryKeyRelatedField(source='parent')

    class Meta:
        model = Category
        fields = ("id", "parent_id", "name", "color", "sorting", "active",
                  "image", "archived")


class PaginatedCategorySerializer(PaginationWithDbSerializer):

    class Meta:
        object_serializer_class = CategorySerializer


class TaxRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaxRate


class PrinterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Printer
        fields = ("id", "name", "local_ip")


class TimeClockSerializer(serializers.ModelSerializer):
    time_in = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    time_out = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = TimeClock
        fields = ("id", "employee", "time_in", "time_out")


class PaginatedTimeClockSerializer(PaginationWithDbSerializer):

    class Meta:
        object_serializer_class = TimeClockSerializer


class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = (
            'name',
            'store',
            'points_redeem',
            'discount',
            'discount_type',
            'discount_type_item',
            # 'discount_type_invoice',
            'discount_text'
        )


class PaginatedRewardSerializer(PaginationWithDbSerializer):

    class Meta:
        object_serializer_class = RewardSerializer


class PaginatedPrinterSerializer(PaginationWithDbSerializer):

    class Meta:
        object_serializer_class = PrinterSerializer


class AddPrinterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Printer
        fields = ("name", "local_ip")


class PaginatedTaxRateSerializer(PaginationWithDbSerializer):

    class Meta:
        object_serializer_class = TaxRateSerializer


class ModifierSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(source="group", many=True)

    class Meta:
        model = Modifier
        fields = ("id", "groups", "name", "cost", "price", "active",
                  "archived")


class PaginatedModifierSerializer(PaginationWithDbSerializer):

    class Meta:
        object_serializer_class = ModifierSerializer


class ModifierGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = ModifierGroup


class PaginatedModifierGroupSerializer(PaginationWithDbSerializer):

    class Meta:
        object_serializer_class = ModifierGroupSerializer


class ProductSerializer(serializers.ModelSerializer):
    tax_rate_id = serializers.PrimaryKeyRelatedField(source='tax_rate')

    class Meta:
        model = Product
        fields = ("id", "name", "image", "color", "sorting", "cost",
                  "price", "barcode", "stock", "tax_rate_id",
                  "active", "price_adjust", "archived", "printer")


class ProductIdNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name")

    def to_native(self, data):
        return {'value': data.id, 'text': data.name}


class PaginatedProductSerializer(PaginationWithDbSerializer):

    class Meta:
        object_serializer_class = ProductSerializer


class DiscountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Discount


class PaginatedDiscountSerializer(PaginationWithDbSerializer):

    class Meta:
        object_serializer_class = DiscountSerializer


class StoreCreatorAPISerializer(serializers.ModelSerializer):
    tax_rate = serializers.PrimaryKeyRelatedField(source='tax_rate')

    class Meta:
        model = Store
        fields = ("id", "name", "logo", "number", "address", "address_2",
                  "city", "state", "zipcode", "phone", "fax", "email", "website", "timezone",
                  "tax_rate", "package", 'xweb_url', 'xweb_terminal_id', 'xweb_id', 'xweb_auth_key', 'xweb_industry')


class StoreSerializer(serializers.ModelSerializer):
    tax_rate_id = serializers.PrimaryKeyRelatedField(source='tax_rate')

    class Meta:
        model = Store
        fields = ("id", "name", "logo", "number", "address", "address_2",
                  "city", "state", "zipcode", "phone", "fax", "email", "website",
                  "tax_rate_id", "package", 'xweb_url', 'xweb_terminal_id', 'xweb_id', 'xweb_auth_key', 'xweb_industry')


class PaginateStoreSerializer(PaginationWithDbSerializer):

    class Meta:
        object_serializer_class = StoreSerializer


class TableSerializer(serializers.ModelSerializer):
    section_id = serializers.PrimaryKeyRelatedField(source='section')
    current_order_id = serializers.PrimaryKeyRelatedField(
        source='current_order')

    class Meta:
        model = Table
        fields = ("id", "section_id", "table_name", "table_image", "x_value",
                  "y_value", "number_people", "archived",
                  "current_order_id")


class PaginateTableSerializer(PaginationWithDbSerializer):

    class Meta:
        object_serializer_class = TableSerializer


class TableSectionSerializer(serializers.ModelSerializer):
    store_id = serializers.PrimaryKeyRelatedField(source='store')

    class Meta:
        model = TableSection
        fields = ("id", "section_name", "store_id")


class PaginateTableSectionSerializer(PaginationWithDbSerializer):

    class Meta:
        object_serializer_class = TableSectionSerializer


class TerminalSerializer(serializers.ModelSerializer):
    # timezone = serializers.SerializerMethodField('get_timezone')
    #
    # def get_timezone(self,val):
    #   return Store.objects.get(pk=1).timezone

    class Meta:
        model = Terminal


class PaginateTerminalSerializer(PaginationWithDbSerializer):

    class Meta:
        object_serializer_class = TerminalSerializer


class Prog2CatSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(source='product')
    category_id = serializers.PrimaryKeyRelatedField(source='category')

    class Meta:
        model = Product.categories.through
        fields = ("id", "product_id", "category_id")


class PaginatedProg2CatSerializer(PaginationWithDbSerializer):

    class Meta:
        object_serializer_class = Prog2CatSerializer


class Prog2MgSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(source='product')
    modifiergroup_id = serializers.PrimaryKeyRelatedField(
        source='modifiergroup')

    class Meta:
        model = Product.modifier_groups.through
        fields = ("id", "product_id", "modifiergroup_id")


class PaginateProg2MgSerializer(PaginationWithDbSerializer):

    class Meta:
        object_serializer_class = Prog2MgSerializer


# add serializers

class AddOrderSerializer(serializers.ModelSerializer):
    emp_open_id = serializers.PrimaryKeyRelatedField(source='emp_open')  # TODO: Should it be required?
    emp_close_id = serializers.PrimaryKeyRelatedField(source='emp_close', required=False)
    shift_id = serializers.PrimaryKeyRelatedField(source='shift', required=False)

    class Meta:
        model = Order
        fields = ("number", "subtotal", "tax_total", "discount_total", "customer",
                  "grand_total", "balance_remaining", "open_date", "hold_date",
                  "close_date", "status", "description", "emp_open_id",
                  "emp_close_id", "discount_orders", "terminal_id", 'shift_id')


class AddPaymentSerializer(serializers.ModelSerializer):
    order_id = serializers.PrimaryKeyRelatedField(source='order')
    employee_id = serializers.PrimaryKeyRelatedField(source='employee')
    shift_id = serializers.PrimaryKeyRelatedField(source='shift', required=False)

    class Meta:
        model = Payment
        fields = ("id", "order_id", "amount", "amount_paid", "tips", "change_amount", "payment_type", "employee_id",
                  "payment_date", "payment_form", "transaction_type", "processor_response", "batch_num",
                  "approval_code", "transaction_id", "terminal_id", "signature", "void_ref", 'shift_id',
                  'check_number')


class AddOrderItemSerializer(serializers.ModelSerializer):
    order_id = serializers.PrimaryKeyRelatedField(source='order')
    product = serializers.PrimaryKeyRelatedField(source='product', required=False)
    employee = serializers.PrimaryKeyRelatedField(source='employee')

    class Meta:
        model = OrderItem
        fields = ("order_id", "name", "price", "cost", "discount", "tax",
                  "void_status", "employee", "product", "quantity", "terminal_id")


class AddOrderModifierSerializer(serializers.ModelSerializer):
    item_id = serializers.PrimaryKeyRelatedField(source='item')
    group_id = serializers.PrimaryKeyRelatedField(source='group')
    oryginal_id = serializers.PrimaryKeyRelatedField(source='oryginal')

    class Meta:
        model = OrderModifier
        fields = ("item_id", "name", "cost",
                  "price", "oryginal_id", "group_id", 'void_status')


class EmployeeShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'name')


class DetailedOrderSerializer(serializers.ModelSerializer):
    emp_open = EmployeeShortSerializer()
    emp_close = EmployeeShortSerializer()
    items = OrderItemSerializer(many=True)
    payments = PaymentSerializer(many=True)
    shift_id = serializers.PrimaryKeyRelatedField(source='shift')

    class Meta:
        model = Order
        fields = (
            'id', 'number', 'subtotal', 'tax_total', 'discount_total', 'grand_total', 'balance_remaining',
            'open_date', 'hold_date', 'close_date', 'status', 'description', 'emp_open', 'emp_close', 'terminal_id',
            'items', 'payments', "customer", "shift_id"
        )


class PaginateDetailedOrderSerializer(PaginationWithDbSerializer):

    class Meta:
        object_serializer_class = DetailedOrderSerializer


class DetailedTableSerializer(serializers.ModelSerializer):
    section = TableSectionSerializer()
    current_order = OrderSerializer()

    class Meta:
        model = Table
        fields = ("id", "section", "table_name", "table_image", "x_value",
                  "y_value", "number_people", "archived",
                  "current_order")


class PaginateDetailedTableSerializer(PaginationWithDbSerializer):

    class Meta:
        object_serializer_class = DetailedTableSerializer


class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = ('id', 'size_x', 'size_y', 'row', 'col')


class ShiftSerializer(serializers.ModelSerializer):
    terminal_id = serializers.PrimaryKeyRelatedField(source='terminal')
    open_shift_employee_id = serializers.PrimaryKeyRelatedField(source='open_shift_employee')
    close_shift_employee_id = serializers.PrimaryKeyRelatedField(source='close_shift_employee', required=False)

    class Meta:
        model = Shift
        fields = (
            'id',
            'terminal_id',
            'open_shift_employee_id',
            'close_shift_employee_id',
            'shift_open_date',
            'shift_update_date',
            'shift_close_date',
            'opening_amount',
            'total_cashtenders',
            'total_cashreturns',
            'total_drops',
            'total_payouts',
            'closing_amount',
            'over_shortage',
        )


class PaginatedShiftSerializer(PaginationWithDbSerializer):
    class Meta:
        object_serializer_class = ShiftSerializer


class AddShiftSerializer(serializers.ModelSerializer):
    terminal_id = serializers.PrimaryKeyRelatedField(source='terminal')
    open_shift_employee_id = serializers.PrimaryKeyRelatedField(source='open_shift_employee')
    close_shift_employee_id = serializers.PrimaryKeyRelatedField(source='close_shift_employee', required=False)

    class Meta:
        model = Shift
        fields = (
            'id',
            'terminal_id',
            'open_shift_employee_id',
            'close_shift_employee_id',
            'shift_open_date',
            'shift_update_date',
            'shift_close_date',
            'opening_amount',
            'total_cashtenders',
            'total_cashreturns',
            'total_drops',
            'total_payouts',
            'closing_amount',
            'over_shortage',
        )


class TaskinGroupSerializer(serializers.ModelSerializer):

    def to_native(self, data):
        return {'value': data.id, 'text': data.name}

    class Meta:
        model = CustomerGroup
        fields = ('name', 'id')


class PaginatedTaskinGroupSerializer(PaginationWithDbSerializer):
    class Meta:
        object_serializer_class = TaskinGroupSerializer


class PayoutSerializer(serializers.ModelSerializer):
    terminal_id = serializers.PrimaryKeyRelatedField(source='terminal')
    employee_id = serializers.PrimaryKeyRelatedField(source='employee')
    shift_id = serializers.PrimaryKeyRelatedField(source='shift', required=False)

    class Meta:
        model = Payout
        fields = (
            'id',
            'employee_id',
            'shift_id',
            'terminal_id',
            'payout_type',
            'payout_value',
            'payout_time',
            'payout_note',
        )


class PaginatedPayoutSerializer(PaginationWithDbSerializer):
    class Meta:
        object_serializer_class = PayoutSerializer


class AddPayoutSerializer(serializers.ModelSerializer):
    terminal_id = serializers.PrimaryKeyRelatedField(source='terminal')
    employee_id = serializers.PrimaryKeyRelatedField(source='employee')
    shift_id = serializers.PrimaryKeyRelatedField(source='shift', required=False)

    class Meta:
        model = Payout
        fields = (
            'id',
            'employee_id',
            'shift_id',
            'terminal_id',
            'payout_type',
            'payout_value',
            'payout_time',
            'payout_note',
        )
