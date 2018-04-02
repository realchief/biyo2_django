from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views import generic as cbv
from panel.views import ShowStock
from payments.views import AddTips
from django.conf.urls.i18n import i18n_patterns


admin.autodiscover()
# TODO: Split urls to own apps.
# urlpatterns = i18n_patterns(
urlpatterns = patterns(
    '',
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^$', cbv.RedirectView.as_view(pattern_name='dashboard')),
    url(r'^stock/', ShowStock.as_view()),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('panel.urls')),
    url(r'^', include('displays.urls')),
    url(r'^reports/', include('reports.urls')),
    url(r'^accounts/login/$', auth_views.login, {'template_name': 'account/login.html'}, name='login'),
    url(r'^accounts/logout/$', auth_views.logout_then_login, name='logout'),
    url(r'^accounts/password_reset/$', auth_views.password_reset, {'template_name': 'account/password_reset.html'}, name='password_reset'),
    url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'account/password_reset_done.html'}, name='password_reset_done'),
    # Support old style base36 password reset links; remove in Django 1.7
    # url(r'^reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$','django.contrib.auth.views.password_reset_confirm_uidb36',{'template_name': 'account/password_reset_confirm.html'}),
    # url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$','django.contrib.auth.views.password_reset_confirm',{'template_name': 'account/password_reset_confirm.html'},name='password_reset_confirm'),
    # NOTE: Why not use django auth logic ? Also, why not store each urls in own app ?
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm',
        name='password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'account/password_reset_complete.html'}, name='password_reset_complete'),
    url(r'^terminalapi/', include('terminalapi.urls')),
    url(r'^addtips/(?P<pk>\d+)/$', AddTips.as_view(), name='add_tips'),
    url(r'^quick/', include('purchase.urls', namespace='quick')),
    url(r'^mobile-api/', include('mobile_api.urls'))
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
    static(settings.STORAGE_URL, document_root=settings.STORAGE_ROOT)

# urlpatterns = patterns(
#     '',
#     url(r'^i18n/', include('django.conf.urls.i18n'))
# ) + i18n_patterns(
#     '',
#     include(urlpatterns),
# )
