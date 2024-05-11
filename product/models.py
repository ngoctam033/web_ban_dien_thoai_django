from django.db import models

class Product(models.Model):
    #id sản phẩm
    product_id = models.AutoField(primary_key=True)
    #tên hãng sản xuất
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, to_field='name', db_column='brand')
    #tên sản phẩm
    name = models.CharField(max_length=100)
    #năm sản xuất
    year = models.IntegerField()
    #xuất xứ
    origin = models.CharField(max_length=100)
    #mô tả sản phẩm
    description = models.TextField()
    #hệ điều hành
    os = models.CharField(max_length=100)
    #giá sản phẩm
    price = models.DecimalField(max_digits=10, decimal_places=2)
    #thông số kỹ thuật
    cpu = models.CharField(max_length=100)
    camera = models.CharField(max_length=100)
    ram = models.CharField(max_length=100)
    rom = models.CharField(max_length=100)
    screen = models.CharField(max_length=100)
    battery = models.IntegerField()
    #ảnh sản phẩm
    image = models.ImageField()
    class Meta:
        db_table = "product"

    def __str__(self):
        return str(self.product_id)
#class lưu tên hãng sản xuất
class Brand(models.Model):
    #tên hãng sản xuất
    name = models.CharField(max_length=100, unique = True)
    #hình ảnh hãng sản xuất
    image_url = models.CharField(max_length=100)
    class Meta:
        db_table = "phone_brands"
    def __str__(self):
        return self.name