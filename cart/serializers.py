from rest_framework import serializers
from .models import Order, OrderItem, Cart

#tạo class OrderItemSerializer
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

#tạo class OrderSerializer
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

#tạo class CartSerializer
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'