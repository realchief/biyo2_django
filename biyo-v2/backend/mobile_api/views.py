from rest_framework import permissions
from rest_framework.filters import SearchFilter, DjangoFilterBackend, OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from mobile_api.serializers import ProductSerializer, CategorySerializer
from products.models import Product, Category


class ProductViewSet(ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    search_fields = ('name',)
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        categories = request.DATA.get('categories')
        if categories and not isinstance(categories, list):
            return Response({'details': 'Categories must be a list'})
        return super(ProductViewSet, self).create(request, *args, **kwargs)


class CategoryViewSet(ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    search_fields = ('name',)
    permission_classes = (permissions.IsAuthenticated,)


class CheckBarcode(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        barcode = request.DATA.get('barcode')
        if barcode:
            if Product.objects.filter(barcode=barcode, archived=0).exists():
                return Response({
                    'response': Product.objects.filter(barcode=barcode, archived=0).first().id
                })
            else:
                return Response({'details': ['Does not exist']})
        else:
            return Response({'details': ['No barcode are entered']})


class CheckEmployeePin(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        pin = request.DATA.get('pin')
        if pin and request.user.pin == pin:
            return Response({'response': ['Success']})
        else:
            return Response({'response': ['Incorrect pin']})
