import json
from django.shortcuts import render
import logging

#tạo một view để nhận data từ client và trả về kết quả
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views import View
from .serializers import CustomerSerializer
from django.contrib.auth import login, logout
from django.urls import reverse
from .backends import EmailBackend
from django.http import JsonResponse
from .models import Customer
from cart.models import Order, OrderItem
from product.models import Product
from cdtt2.logger import logger

from django.contrib.auth.decorators import login_required



#lớp này dùng để tạo tài khoản cho khách hàng
class CustomerView(APIView):
    #phương thức post
    def post(self, request):
        #get data from client
        first_name = request.data.get('ho')
        last_name = request.data.get('ten')
        email = request.data.get('email')
        password = request.data.get('newPass')
        tel = request.data.get('soDienThoai')
        username = username = first_name + ' ' + last_name

        #đưa data vào serializer
        serializer = CustomerSerializer(data={
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'email': email,
            'password': password,
            'tel': tel
        })
        # xác thực data
        if serializer.is_valid():
            # lưu data vào database
            user = serializer.create(serializer.validated_data)
            
            # đăng nhập người dùng
            login(request, user, backend='customer.backends.EmailBackend')
            logger.info('Tạo tài khoản thành công')
            return Response({"status": "success", "message": "Account created successfully."}, status=200)
        else:
            # thông báo cho client biết tạo tài khoảng thất bại
            logging.error('Tạo tài khoản thất bại')
            logging.error('Lỗi từ serializer: %s', serializer.errors)
            error_message = serializer.errors['email'][0] if 'email' in serializer.errors else 'Unknown error'
            return Response({"status": "failed", "message": error_message}, status=400)
    
#lớp này dùng để trả về trang customer, khi người dùng click vào nút customer
class CustomerFromView(View):
    def get(self, request):
        if request.user.is_authenticated:
            #lấy customer_id của user
            customers_id = request.user.customers_id
            customer = Customer.objects.get(customers_id=customers_id)
            orders = Order.objects.filter(customer_id=customers_id).order_by('-order_id')

            order_context = {}
            for order in orders:
                order_items = OrderItem.objects.filter(order_id=order.order_id)
                products = []
                for item in order_items:
                    product_info = {
                        'ten_san_pham': item.product_id.name,
                        'so_luong': item.quantity,
                        'gia': item.price,
                        'ngay_dat_hang': order.date,
                        'trang_thai_giao_hang': order.status,
                    }
                    products.append(product_info)
                order_context[order.order_id] = products

            return render(request, 'customer.html', {'customer': customer, 'orders': order_context})
        else:
            return render(request, 'login.html')   
#lớp này dùng để trả về trang login, khi người dùng click vào nút đăng nhập
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        #in ra email và password để kiểm tra

        user = EmailBackend.authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user, backend='customer.backends.EmailBackend')
            return JsonResponse({"status": "success", "message": "User logged in"})
        else:
            return JsonResponse({"status": "error", "message": "Invalid username or password"}, status=400)

#lớp này dùng để trả về trang signup, khi người dùng click vào nút đăng ký
class SignupView(View):
    def get(self, request):
        return render(request, 'Signup.html')
    
#lớp này dùng để đăng xuất khỏi tài khoản
class LogoutView(View):
    def post(self, request):
        logout(request)
        if request.user.is_authenticated:
            # Nếu người dùng vẫn đang đăng nhập sau khi gọi logout(), có lỗi xảy ra
            return JsonResponse({'message': 'Lỗi: Không thể đăng xuất khỏi tài khoản'}, status=500)
        else:
            # Nếu người dùng đã đăng xuất thành công, trả về thông báo thành công
            return JsonResponse({'message': 'Đăng xuất thành công'}, status=200)

    
#tạo một api để kiểm tra xem người dùng đã đăng nhập chưa
class CheckLoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return JsonResponse({'login': True})
        else:
            return JsonResponse({'login': False})
        
@login_required
def get_username(request):
    return JsonResponse({'username': request.user.first_name + ' ' + request.user.last_name})

#tạo một api để thay đổi địa chỉ
class ChangeAddressView(View):
    def post(self, request):
        try:
            # Lấy địa chỉ mới từ client
            data = json.loads(request.body)
            new_address = data.get('address')

            # Thay đổi địa chỉ
            request.user.address = new_address
            request.user.save()
            return JsonResponse({'message': 'Thay đổi địa chỉ thành công'}, status=200)
        except Exception as e:
            # Trả về thông báo lỗi nếu có lỗi xảy ra
            return JsonResponse({'message': str(e)}, status=400)
        
#tao api de thay doi so dien thoai
class ChangeTelView(View):
    def post(self, request):
        try:
            # Lấy số điện thoại mới từ client
            data = json.loads(request.body)
            new_tel = data.get('phone_number')

            # Thay đổi số điện thoại
            request.user.tel = new_tel
            request.user.save()
            return JsonResponse({'message': 'Thay đổi số điện thoại thành công'}, status=200)
        except Exception as e:
            # Trả về thông báo lỗi nếu có lỗi xảy ra
            return JsonResponse({'message': str(e)}, status=400)
        
#lớp này dùng để đổi mật khẩu
class ChangePasswordView(View):
    def post(self, request):
        try:
            # Lấy mật khẩu mới và mật khẩu cũ từ client
            data = json.loads(request.body)
            new_password = data.get('new_password')
            old_password = data.get('old_password')
            # Kiểm tra mật khẩu cũ
            if not request.user.check_password(old_password):
                return JsonResponse({'message': 'Mật khẩu cũ không đúng'}, status=200)
            # Thay đổi mật khẩu
            request.user.set_password(new_password)
            request.user.save()
            return JsonResponse({'message': 'Thay đổi mật khẩu thành công'}, status=200)
        except Exception as e:
            # Trả về thông báo lỗi nếu có lỗi xảy ra
            return JsonResponse({'message': str(e)}, status=200)