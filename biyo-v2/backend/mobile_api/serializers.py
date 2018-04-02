from django.core.exceptions import ValidationError
from rest_framework import serializers
from products.models import Product, Category, TaxRate


class ProductSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(required=True, many=True)

    def __init__(self, *args, **kwargs):
        super(ProductSerializer, self).__init__(*args, **kwargs)
        # XXX: TaxRate table maybe clean.
        self.fields["tax_rate"].initial = TaxRate.objects.get(id=1)
        self.fields["tax_status"].initial = 1
        if 'instance' in kwargs:
            try:
                self.id = kwargs['instance'].id
            except AttributeError:
                pass

    def validate_categories(self, attrs, *args, **kwargs):
        categories = attrs.get('categories')
        if not categories or not isinstance(categories, list):
            raise ValidationError({'categories': ['Must be selected at least one category']})
        return attrs

    def validate_barcode(self, attrs, *args, **kwargs):
        if self.context.get('request').method == 'POST':
            barcode = attrs.get('barcode', '')
            if barcode == "" or barcode == "0.0":
                return attrs
            qs = Product.objects.filter(barcode=barcode).exclude(archived=True)
            try:
                if self.id:
                    qs = qs.exclude(pk=self.id)
            except AttributeError:
                pass
            if qs.count() > 0:
                raise ValidationError({"barcode": ["This barcode is already in use."]})
        return attrs

    def save(self, *args, **kwargs):
        if self.object.id:
            self.object.change_reason = "Update product"
        else:
            self.object.change_reason = "Create product"
        self.object.stock_change = 0
        return super(ProductSerializer, self).save(**kwargs)

    class Meta:
        model = Product
        fields = ("id", "name", "image", "color", "sorting", "cost",
                  "price", "barcode", "stock", "tax_status", "tax_rate",
                  "active", "price_adjust", "archived", "print_to", "printer",
                  "categories")


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ("id", "name", "color", "sorting", "active",
                  "image", "archived")
