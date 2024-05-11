from django.db import models
from customer.models import Customer


# Create your models here.
#tạo class Order
class Order(models.Model):
    STATUS =(
        ('Đang chờ xác nhận','Đang chờ xác nhận'),
        ('Đã xác nhận','Đã xác nhận'),
        ('Đang giao hàng','Đang giao hàng'),
        ('Đã giao thành công','Đã giao thành công'),
    )
    order_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey('customer.Customer', on_delete=models.CASCADE, to_field='customers_id', db_column='customer_id')
    address = models.CharField(max_length=200, default='No address provided')
    date = models.DateTimeField()
    status=models.CharField(max_length=50,null=True,choices=STATUS, default='Đang chờ xác nhận')

    class Meta:
        db_table = "orders"
    
    def __str__(self):
        return str(self.order_id)

#tạo class OrderItem
class OrderItem(models.Model):
    order_item_id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey('Order', on_delete=models.CASCADE, db_column='order_id')
    product_id = models.ForeignKey('product.Product', on_delete=models.CASCADE, to_field='product_id', db_column='product_id')
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "order_items"
        unique_together = ('order_id', 'product_id')
#tạo một class để lưu sản phẩm trong giỏ hàng   
class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    customers_id = models.ForeignKey('customer.Customer', on_delete=models.CASCADE, to_field='customers_id', db_column='customers_id')
    product_id = models.ForeignKey('product.Product', on_delete=models.CASCADE, to_field='product_id', db_column='product_id')
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "cart"