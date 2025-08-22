from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, product_list_page, product_detail_page

app_name = 'products'

router = DefaultRouter()
router.register('api/products', ProductViewSet, basename='product')

urlpatterns = [
    # API
    path('', include(router.urls)),
    # HTML
    path('list/', product_list_page, name='list'),
    path('<int:pk>/', product_detail_page, name='detail'),
]
