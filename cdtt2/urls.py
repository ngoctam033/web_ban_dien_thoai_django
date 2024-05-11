"""
URL configuration for cdtt2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from contact.views import ContactView
from product.views import ProductView, BrandView, ProductSearchView, ProductDetailView, SearchView, ProductFilterView
from cart.views import CartView,CreateCartView, CreateOrderView, cart_count, delete_product
from cdtt2.views import FAQsView, HomeView, ReturnPolicyView, ShippingInforView, ShoppingGuideView, SupportView, WarrantyView, AboutUsView, get_json_data
from customer.views import CustomerView,CheckLoginView,LogoutView,LoginView, get_username, CustomerFromView,ChangePasswordView, ChangeAddressView, ChangeTelView
from django.contrib.auth import views as auth_views

urlpatterns = [
    #trả về trang chủ
    path('', HomeView.as_view(), name='home'),
    #trả về trang product
    path('product-detail/<str:product_name>/', ProductDetailView.as_view(), name='product_detail'),
    #trả về trang liên hệ
    path('contact/', ContactView.as_view(), name='contact'),
    #trả về trang hỗ trợ
    path('support/', SupportView.as_view(), name='support'),
    #trả về trang hướng dẫn mua sắm
    path('shopping_guide/', ShoppingGuideView.as_view(), name='shopping_guide'),
    #trả về trang chính sách đổi trả
    path('return_policy/', ReturnPolicyView.as_view(), name='return_policy'),
    #trả về trang thông tin vận chuyển
    path('shipping_infor/', ShippingInforView.as_view(), name='shipping_infor'),
    #trả về trang câu hỏi thường gặp
    path('faqs/', FAQsView.as_view(), name='faqs'),
    #trả về trang giới thiệu
    path('about_us/', AboutUsView.as_view(), name='about_us'),
    #tạo url cho api lọc sản phẩm
    path('products/', ProductFilterView.as_view(), name='product_filter'),
    #trả về trang tìm kiếm
    path('search/', SearchView.as_view(), name='search'),
    #trả về trang bảo hành
    path('warranty_center/', WarrantyView.as_view(), name='warranty'),
    #api để tìm kiếm sản phẩm
    path('api/search/', ProductSearchView.as_view(), name = 'search_product'),
    #api để lấy data product từ database
    path('api/products/<int:page_number>/', ProductView.as_view(), name='product_list'),
    #api để lấy data brand từ database
    path('api/brands/', BrandView.as_view(), name='brand_list'),
    #api trả về danh sách sản phẩm theo hãng
    #api để tạo tài khoảng customer
    path('api/customer/', CustomerView.as_view(), name='create_customer'),
    #api để thực hiện đăng xuất
    path('logout/', LogoutView.as_view(), name='logout'),
    #api để kiểm tra xem người dùng đã đăng nhập chưa
    path('api/check-login/', CheckLoginView.as_view(), name='check_login'),
    #api để lấy tên người dùng
    path('api/get_username/', get_username, name='get_username'),
    path('social/', include('social_django.urls', namespace='social')),  # <-- Đăng ký namespace ở đây
    #api login
    path('api/login/', LoginView.as_view(), name='login'),
    #url cho trang giỏ hàng
    path('cart/', CartView.as_view(), name='cart'),
    #path api để thêm sản phẩm vào giỏ hàng
    path('api/add-to-cart/', CreateCartView.as_view(), name='add_to_cart'),
    #api trả về tổng số sản phẩm trong giỏ hàng
    path('api/cart-count/', cart_count, name='cart_count'),
    #tạo api để tạo order
    path('api/create-order/', CreateOrderView.as_view(), name='create_order'),
    #tạo url để thữ hiện xóa một sản phẩm trong giỏe hàng
    path('api/delete_product/', delete_product, name='delete_cart'),
    #tạo path để trả về trang customer
    path('customer/', CustomerFromView.as_view(), name='customer'),
    #tạo url để thay đổi mật khẩu
    path('api/change-password/', ChangePasswordView.as_view(), name='change_password'),
    #api để đổi địa chỉ
    path('api/change-address/', ChangeAddressView.as_view(), name='change_address'),
    #api để đổi số điện thoại
    path('api/change-tel/', ChangeTelView.as_view(), name='change_tel'),

    #url cho password reset
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    #url cho admin
    path('admin/', admin.site.urls),
        # Cấu hình URL để phục vụ file JSON
    path('data.json', get_json_data, name='get_json_data'),
]
