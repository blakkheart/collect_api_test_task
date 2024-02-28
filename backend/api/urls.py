from django.urls import include, path
from django.conf import settings
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from api.views import (
    ReasonViewSet,
    CollectViewSet,
    PaymentViewSet,
)

router_v1 = DefaultRouter()

router_v1.register(r'reasons', ReasonViewSet, basename='reasons')
router_v1.register(r'collections', CollectViewSet, basename='collections')
router_v1.register(
    r'collections/(?P<collection_id>\d+)/payments',
    PaymentViewSet,
    basename='payments'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include('djoser.urls')),
    path('v1/auth/', include('djoser.urls.authtoken')),
    path('v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'v1/docs/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='docs'
    ),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
