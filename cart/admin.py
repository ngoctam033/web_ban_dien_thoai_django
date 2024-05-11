from django.contrib import admin
from .models import Order, OrderItem, Cart,Customer
from product.models import Product
from .models import OrderItem
from django.contrib import admin


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'get_customer_name', 'date', 'status']
    ordering = ['order_id']

    def get_customer_name(self, obj):
        return obj.customer_id.username
    get_customer_name.short_description = 'Customer Name'  # Sets column header

    def get_customer_phone(self, obj):
        return obj.customer_id.phone_number
    get_customer_phone.short_description = 'Customer Phone'  # Sets column header

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['get_customer_name','order_item_id', 'order_id', 'get_product_name', 'quantity', 'price']
    ordering = ['order_item_id']

    def get_customer_name(self, obj):
        order = obj.order_id
        return order.customer_id.username
    get_customer_name.short_description = 'Customer Name'  # Sets column header

    def get_product_name(self, obj):
        return obj.product_id.name
    get_product_name.short_description = 'Product ID'  # Sets column header
    
class CartAdmin(admin.ModelAdmin):
    list_display = ['cart_id', 'customer_name', 'customer_email', 'product_name', 'quantity', 'price']
    ordering = ['cart_id']

    def customer_name(self, obj):
        return obj.customers_id.username
    customer_name.short_description = 'Name'  # Sets the column header

    def customer_email(self, obj):
        return obj.customers_id.email
    customer_email.short_description = 'Email'  # Sets the column header

    def product_name(self, obj):
        return obj.product_id.name
    product_name.short_description = 'Product Name'  # Sets the column header

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Cart, CartAdmin)