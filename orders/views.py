# from django.shortcuts import render, redirect
# from rest_framework import viewsets, permissions, status
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from django.db import transaction
# from decimal import Decimal

# from .models import Order, OrderItem
# from .serializers import OrderSerializer
# from cart.models import CartItem

# class OrderViewSet(viewsets.ReadOnlyModelViewSet):
#     """
#     Users can list/retrieve their own orders.
#     Checkout action converts cart -> order.
#     """
#     serializer_class = OrderSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return Order.objects.filter(user=self.request.user).prefetch_related('items__product')

#     @action(detail=False, methods=['post'])
#     def checkout(self, request):
#         user = request.user
#         cart_items = CartItem.objects.filter(user=user).select_related('product')
#         if not cart_items.exists():
#             return render(request, "orders/checkout.html", {"error": "Your cart is empty."})

#         with transaction.atomic():
#             order = Order.objects.create(user=user, status='PENDING', total_price=0)
#             total = Decimal('0.00')
#             for ci in cart_items:
#                 price = ci.product.price
#                 OrderItem.objects.create(
#                     order=order, product=ci.product, quantity=ci.quantity, price=price
#                 )
#                 total += price * ci.quantity
#                 # Optional: decrement stock
#                 if ci.product.stock >= ci.quantity:
#                     ci.product.stock -= ci.quantity
#                     ci.product.save()
#             order.total_price = total
#             order.status = 'COMPLETED'
#             order.save()
#             cart_items.delete()

#         #return redirect('orders/orders.html')  # Redirect to orders page after checkout
#         #eturn render(request, 'orders/orders.html', {'orders': order})
#         return render(request, 'orders/orders.html', {'orders': [order]})



# # Django Template View (HTML)
# def orders_page(request):
#     if request.user.is_authenticated:
#         orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
#     else:
#         orders = []
#     return render(request, "orders/orders.html", {"orders": [orders]})





from django.shortcuts import render, redirect
from rest_framework import viewsets, permissions
from django.db import transaction
from decimal import Decimal

from .models import Order, OrderItem
from .serializers import OrderSerializer
from cart.models import CartItem


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Users can list/retrieve their own orders via API.
    Checkout converts cart -> order.
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product')

    # Checkout action for POST
    def checkout(self, request):
        user = request.user
        cart_items = CartItem.objects.filter(user=user).select_related('product')
        if not cart_items.exists():
            return redirect("orders_page")  # Cart empty → just redirect

        with transaction.atomic():
            order = Order.objects.create(user=user, status='PENDING', total_price=0)
            total = Decimal('0.00')
            for ci in cart_items:
                price = ci.product.price
                OrderItem.objects.create(
                    order=order, product=ci.product, quantity=ci.quantity, price=price
                )
                total += price * ci.quantity
                if ci.product.stock >= ci.quantity:
                    ci.product.stock -= ci.quantity
                    ci.product.save()
            order.total_price = total
            order.status = 'COMPLETED'
            order.save()
            cart_items.delete()

        return redirect("orders_page")  # Redirect to orders page after checkout


# HTML page to list all user orders
def orders_page(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
    else:
        orders = []
    return render(request, "orders/orders.html", {"orders": orders})
