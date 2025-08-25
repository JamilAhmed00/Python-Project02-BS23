

from django.shortcuts import render, redirect
from rest_framework import viewsets, permissions
from .models import CartItem
from .serializers import CartItemSerializer

# DRF ViewSet (API)
class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user).select_related('product')

    def perform_create(self, serializer):
        item, created = CartItem.objects.get_or_create(
            user=self.request.user,
            product=serializer.validated_data['product'],
            defaults={'quantity': serializer.validated_data.get('quantity', 1)}
        )
        if not created:
            item.quantity += serializer.validated_data.get('quantity', 1)
            item.save()
        else:
            serializer.instance = item

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            self.permission_denied(self.request, message="Not your cart item")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            self.permission_denied(self.request, message="Not your cart item")
        instance.delete()


# Django Template View (HTML)
def cart_page(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user).select_related("product")
    else:
        cart_items = []

    total_price = sum([item.product.price * item.quantity for item in cart_items])
    return render(request, "cart/cart.html", {"cart_items": cart_items, "total_price": total_price})
