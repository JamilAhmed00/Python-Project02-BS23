from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartItemViewSet
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

app_name = 'cart'

router = DefaultRouter()
router.register('api/cart', CartItemViewSet, basename='cart')

# Simple HTML cart page
@login_required
def cart_page(request):
    return render(request, 'cart/cart.html')

urlpatterns = [
    path('', include(router.urls)),
    path('', cart_page, name='page'),
]
