from django.conf.urls import patterns, url, include

from displays.views import BasicVersionCreateView, PictureDeleteView,PictureListView, weather
from views import TweetList, YelpReviewList, LastCheckIn, CategoryProductList, ProductView, display_crud, box_crud, element_crud

urlpatterns = patterns('',
    url(r'^', include(display_crud.urls)),
    url(r'^', include(box_crud.urls)),
    url(r'^', include(element_crud.urls)),
    url(r'^upload/basic/',BasicVersionCreateView.as_view(),name='upload-picture'),
    url(r'^delete/(?P<pk>\d+)$', PictureDeleteView.as_view(), name='upload-delete'),
    url(r'^upload/view/(?P<pk>\d+)$', PictureListView.as_view(), name='upload-view'),
    #url(r'^displays/$', DisplayListView.as_view(), name='display_list'),
    #url(r'^displays/(?P<pk>\d+)$', DisplayView.as_view(), name='display_detail'),
    url(r'^socialapi/get/product/(?P<pk>\d+)$', ProductView.as_view()),
    url(r'^socialapi/get/tweets', TweetList.as_view()),
    url(r'^socialapi/get/yelp_reviews', YelpReviewList.as_view()),
    url(r'^socialapi/get/last_checkin', LastCheckIn.as_view()),
    url(r'^socialapi/get/category_products', CategoryProductList.as_view()),
    url(r'^weather/get/(?P<zip>\d+)', weather),


)
