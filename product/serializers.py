from rest_framework import serializers
from .models import Product
from .models import Brand

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('image','battery', 'screen','rom','ram','camera','cpu',
                  'price','os','description','origin','year','name','brand')

#tạo serializer cho class Brand
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'