from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem, Cart
from .serializers import OrderSerializer, OrderItemSerializer, CartSerializer
from product.models import Product
from datetime import datetime, date
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum
import pytz
from django.views.decorators.csrf import csrf_exempt

#lớp này dùng để trả về trang cart, khi người dùng click vào nút giỏ hàng
class CartView(APIView):
     def get(self, request):
        try:
            if request.user.is_authenticated:
                cart_items = Cart.objects.filter(customers_id=request.user.customers_id).order_by('cart_id')
    
                # Tạo một danh sách chứa thông tin về tất cả các sản phẩm trong giỏ hàng
                products_in_cart = []
                for item in cart_items:
                    product = item.product_id
                    products_in_cart.append({
                        'name': product.name,
                        'price': product.price,
                        'quantity': item.quantity,
                    })
    
                # Truyền danh sách sản phẩm vào hàm render như một phần của context
                return render(request, 'cart.html', {'products_in_cart': products_in_cart})
            else:
                return render(request, 'cart.html')
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#taoh hàm post để thêm sản phẩm vào giỏ hàng
class CreateCartView(APIView):
    def post(self, request):
        ten_san_pham = request.data.get('ten_san_pham')
        user = request.user

        if user.is_authenticated:
            #truy cập vào database để lấy product_id cửa sản phẩm có tên được lưu trong ten_san_pham
            product_id = Product.objects.get(name=ten_san_pham).product_id
            #truy cập vào database để lấy price của sản phẩm
            price = Product.objects.get(name=ten_san_pham).price
            #lấy customer_id của user
            customers_id = user.customers_id
            #kiếm tra xem sản phẩm đã có trong giỏ hàng chưa
            cart = Cart.objects.filter(customers_id=customers_id, product_id=product_id)
            
            #nếu sản phẩm đã có trong giỏ hàng thì tăng số lượng lên 1
            if cart:
                cart = cart[0]
                cart.quantity += 1
                cart.save()
            #nếu sản phẩm chưa có trong giỏ hàng thì thêm sản phẩm vào giỏ hàng
            else:
                #tạo một serializer để lưu sản phẩm vào giỏ hàng
                serializer = CartSerializer(data ={
                    "customers_id": customers_id,
                    "product_id": product_id,
                    "quantity": 1,
                    "price": price
                })
                #kiểm tra xem dữ liệu có hợp lệ không
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "Sản phẩm đã được thêm thành công"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Bạn cần đăng nhập để thêm sản phẩm vào giỏ hàng"}, status=status.HTTP_401_UNAUTHORIZED)

#tạo api để tạo đơn hàng
class CreateOrderView(APIView):
    #phương thức post để tạo đơn hàng
    def post(self, request):
        #lấy thông tin về user
        user = request.user
        #lấy danh sách sản phẩm trong đơn hàng
        products = request.data.get('selectedProducts')
        
        #tạo oder_id
        order_id  = str(Order.objects.count() % 10000).zfill(4)
        vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        #tạo date order
        date_order = datetime.now(vietnam_tz)
        #lấy customer_id của user
        customers_id = user.customers_id
        #trang thái đơn hàng, true là đã gửi, false là chưa gửi
        order_status = False
        #lấy địa chỉ của user
        address = user.address
        if(address == "No address provided"):
            return Response({"message": "Bạn cần cung cấp địa chỉ để tạo đơn hàng"})
        #lấy số điện thoại của user
        telephone = user.tel
        #kiểm tra số điện thoại
        if(telephone == ""):
            return Response({"message": "Bạn cần cung cấp số điện thoại để tạo đơn hàng"})

        #tạo serializer để lưu thông tin đơn hàng vào database
        serializer_order = OrderSerializer(data ={
            "order_id": order_id,
            "date": date_order,
            "customer_id": customers_id,
            "address": address,
            "status": order_status
        })
        #kiểm tra dữ liệu có hợp lệ không
        if serializer_order.is_valid():
            serializer_order.save()
        else:
            return Response({"error": serializer_order.errors}, status=status.HTTP_400_BAD_REQUEST)
        #duyệt qua từng sản phẩm trong danh sách
        for product in products:
            #lấy product_id của sản phẩm trong database thông qua biến product
            product_id = Product.objects.get(name=product).product_id

            #lấy quantity của sản phẩm trong database thông qua biến product_id
            quantity = Cart.objects.get(customers_id=customers_id, product_id=product_id).quantity

            # lấy price của sản phẩm trong database thông qua biến product_id
            price = Product.objects.get(product_id=product_id).price
            #tạo serializer để lưu thông tin sản phẩm vào database
            serializer_order_item = OrderItemSerializer(data ={
                "order_id": order_id,
                "product_id": product_id,
                "quantity": quantity,
                "price": price
            })
            #kiểm tra dữ liệu có hợp lệ không
            if serializer_order_item.is_valid():
                serializer_order_item.save()
            else:
                return Response({"error": serializer_order_item.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Đơn hàng đã được tạo thành công"}, status=status.HTTP_201_CREATED)
@login_required
def cart_count(request):
    if request.user.is_authenticated:
        count = Cart.objects.filter(customers_id=request.user).aggregate(Sum('quantity'))['quantity__sum'] or 0

        return JsonResponse({'count': count})
    else:
        return JsonResponse({'count': 0})
#tạo api để xem đơn hàng
class OrderView(APIView):
    def get(self, request):
        try:
            if request.user.is_authenticated:
                orders = Order.objects.filter(customer_id=request.user.customers_id).order_by('order_id')
    
                # Tạo một danh sách chứa thông tin về tất cả các sản phẩm trong giỏ hàng
                products_in_order = []
                for item in orders:
                    product = Product.objects.get(product_id=item.product_id)
                    products_in_order.append({
                        'name': product.name,
                        'price': product.price,
                        'quantity': item.quantity,
                    })

    
                # Truyền danh sách sản phẩm vào hàm render như một phần của context
                return render(request, 'order.html', {'products_in_order': products_in_order})
            else:
                

                return render(request, 'order.html')
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
def delete_product(request):
    if request.method == 'POST':
        product_name = request.GET.get('productName')

        if product_name:
            try:
                # Tìm sản phẩm dựa trên tên sản phẩm, trong model cart
                order_item = Cart.objects.get(product_id=Product.objects.get(name=product_name).product_id, customers_id=request.user.customers_id)
                # Xóa sản phẩm
                order_item.delete()
                return JsonResponse({'success': True})
            except Product.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Sản phẩm không tồn tại'})
        else:
            return JsonResponse({'success': False, 'error': 'Tên sản phẩm không được cung cấp'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request'})