from django.shortcuts import render
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, Brand
from .serializers import ProductSerializer, BrandSerializer
from django.core.paginator import Paginator
from django.db.models import Q

#lớp này dùng để trả về danh sách sản phẩm
class ProductView(APIView):
    def get(self, request, page_number):
        try:
            products = Product.objects.all()  # Get all products
            paginator = Paginator(products, 10)  # Show 10 products per page
            if page_number > paginator.num_pages:
                return Response({"error": "NoMoreProduct"})
            products_page = paginator.get_page(page_number)
            serializer = ProductSerializer(products_page, many=True)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({"error": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#lớp này dùng để trả về thông tin chi tiết của sản phẩm
class ProductDetailView(APIView):
    def get(self, request, product_name):
        try:
            product = Product.objects.get(name=product_name)
            product.price = '{:,}'.format(int(product.price)).replace(',', '.')
            return render(request, 'product_detail.html', {'product': product})
        except ObjectDoesNotExist:
            return Response({"error": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class ProductDetailAPIView(APIView):
    def get(self, request, product_name):
        try:
            product = Product.objects.get(name=product_name)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({"error": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#tạo api trả về danh sách được lọc theo các tiêu chí

class ProductFilterView(APIView):
    def get(self, request):
        try:
            # Lấy các tham số truy vấn từ URL
            price = self.request.query_params.get('data-price', None)
            sort = self.request.query_params.get('sort-filter', None)
            ram = self.request.query_params.get('ram-filter', None)
            rom = self.request.query_params.get('rom-filter', None)

            # Tạo một truy vấn Q để lọc sản phẩm
            query = Q()

            # Thêm các tiêu chí lọc vào truy vấn
            if price is not None:
                a, b = map(int, price.split('-'))
                query &= Q(price__gte=a, price__lte=b)
            if ram is not None:
                query &= Q(ram=ram)
            if rom is not None:
                query &= Q(rom=rom)

            # Lọc sản phẩm dựa trên truy vấn
            products = Product.objects.filter(query)

            # Sắp xếp sản phẩm dựa trên tham số sort
            if sort == 'asc':
                products = products.order_by('price')
            elif sort == 'desc':
                products = products.order_by('-price')

            # Serialize và trả về dữ liệu
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({"error": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#tạo class tra về thông tin hãng
class BrandView(APIView):
    def get(self, request):
        try:
            #lấy tất cả các hãng sản xuất
            brands = Brand.objects.values('name','image_url').distinct()
            serializer = BrandSerializer(brands, many=True)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({"error": "Brand does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #tạo hàm trả về danh sách sản sanr phẩm theo hãng
    def product_by_brand(request, brand_name):
        try:
            products = Product.objects.filter(brand=brand_name)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({"error": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#trả về trang tìm kiếm
class SearchView(APIView):
    def get(self, request):
        return render(request, 'search.html')
#tạo api để tìm kiếm sản phẩm
class ProductSearchView(APIView):
    def get(self, request):
        keyword = request.query_params.get('keyword', '')
        try:
            if keyword:
                products = Product.objects.filter(Q(name__icontains=keyword) | Q(description__icontains=keyword))
            else:
                products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

