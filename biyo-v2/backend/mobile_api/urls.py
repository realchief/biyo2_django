from django.conf.urls import url, include, patterns
from rest_framework.routers import DefaultRouter

from mobile_api.views import ProductViewSet, CategoryViewSet, CheckBarcode, CheckEmployeePin

router = DefaultRouter()

router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^check-barcode', CheckBarcode.as_view()),
    url(r'^check-pin', CheckEmployeePin.as_view())
)
