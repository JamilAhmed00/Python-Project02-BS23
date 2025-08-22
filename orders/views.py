from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from decimal import Decimal

from .models import Order, OrderItem
from .serializers import OrderSerializer
from cart.models import CartItem

class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Users can list/retrieve their own orders.
    Checkout action converts cart -> order.
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product')

    @action(detail=False, methods=['post'])
    def checkout(self, request):
        user = request.user
        cart_items = CartItem.objects.filter(user=user).select_related('product')
        if not cart_items.exists():
            return Response({'detail': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            order = Order.objects.create(user=user, status='PENDING', total_price=0)
            total = Decimal('0.00')
            for ci in cart_items:
                price = ci.product.price
                OrderItem.objects.create(
                    order=order, product=ci.product, quantity=ci.quantity, price=price
                )
                total += price * ci.quantity
                # optional: decrement stock
                if ci.product.stock >= ci.quantity:
                    ci.product.stock -= ci.quantity
                    ci.product.save()
            order.total_price = total
            order.status = 'COMPLETED'
            order.save()
            cart_items.delete()

        #return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return render(request, "orders/checkout.html", {"orders": [order]})


