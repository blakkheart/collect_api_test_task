from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    ReasonViewSet,
    CollectViewSet,
    PaymentViewSet,
)

router_v1 = DefaultRouter()

router_v1.register(r'reasons', ReasonViewSet, basename='reasons')
router_v1.register(r'collections', CollectViewSet, basename='collections')
router_v1.register(r'collections/(?P<collection_id>\d+)/payments',
                   PaymentViewSet, basename='payments')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
