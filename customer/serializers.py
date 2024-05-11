from rest_framework import serializers
from .models import Customer
from django.contrib.auth.hashers import make_password

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['username','first_name','last_name', 'email', 'password', 'tel']
    
    def create(self, validated_data):
        #mã hóa mật khẩu
        validated_data['password'] = make_password(validated_data['password'])
        return Customer.objects.create(**validated_data)