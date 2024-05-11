from django.contrib import admin
from contact.models import Contact
from product.models import Product
from cart.models import Order, OrderItem, Cart
from customer.models import Customer

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Contact)
# Register your models here.