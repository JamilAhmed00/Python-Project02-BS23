from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import CartItem
from .serializers import CartItemSerializer

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
