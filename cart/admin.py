from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CartItem

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id','user','product','quantity','added_at')
    list_select_related = ('user','product')
