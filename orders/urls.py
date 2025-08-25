# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import OrderViewSet

# app_name = 'orders'

# router = DefaultRouter()
# router.register('api/orders', OrderViewSet, basename='orders')

# urlpatterns = [
#     path('', include(router.urls)),
    
# ]



# orders/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, orders_page

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')


urlpatterns = [
    path('', include(router.urls)),
    # Checkout button → POST request to /orders/checkout/
    path('orders/checkout/', OrderViewSet.as_view({'post': 'checkout'}), name='checkout'),
    path("orders-page/", orders_page, name="orders_page"),

]
