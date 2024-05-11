#import các thư viện cần thiết
from django.shortcuts import render
from django.views import View
from django.template import TemplateDoesNotExist
from django.http import JsonResponse
import json
#lớp này dùng để trả về trang chủ web, khi người dùng truy cập vào trang web
class HomeView(View):
    def get(self, request):
        try:
            return render(request, 'home.html')
        except TemplateDoesNotExist:
            return render(request, 'error.html', {'message': 'Home page not found'}, status=404)
        except Exception as e:
            return render(request, 'error.html', {'message': str(e)}, status=500)

#tạo class để trả về trang bảo hành
class WarrantyView(View):
    def get(self, request):
        try:
            return render(request, 'warranty_center.html')
        except TemplateDoesNotExist:
            return render(request, 'error.html', {'message': 'Warranty page not found'}, status=404)
        except Exception as e:
            return render(request, 'error.html', {'message': str(e)}, status=500)
#tạo class để trả về trang giới thiệu
class AboutUsView(View):
    def get(self, request):
        try:
            return render(request, 'about_us.html')
        except TemplateDoesNotExist:
            return render(request, 'error.html', {'message': 'AboutUs page not found'}, status=404)
        except Exception as e:
            return render(request, 'error.html', {'message': str(e)}, status=500)

def get_json_data(request):
    #lấy tham số từ request
    province_id = request.GET.get('province_id', None)
    #lấy tham số quận huyện
    district_id = request.GET.get('district_id', None)

    # Đọc nội dung từ file data.json
    with open('./statics/store/js/Province.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    #nếu tồn tại tham số district_id, trả về dữ liệu theo district_id
    if district_id:
        for city in data:
            for district in city['Districts']:
                if district['Id'] == district_id:
                    # Lấy danh sách các phường
                    data = [{ 'Id': ward['Id'], 'Name': ward['Name'] } for ward in district['Wards']]

                    break
            else:
                continue
            break
        else:
            #trả về json thông báo
            return JsonResponse({'message': f"District with ID {district_id} not found"}, status=404)
    #nếu tồn tại tham số province_id, trả về dữ liệu theo province_id
    if province_id is not None:
        for city in data:
            if city['Id'] == province_id:
                data = city['Districts']
                break
        else:
            return JsonResponse({'message': f"Province with ID {province_id} not found"}, status=404)
    
    return JsonResponse(data, safe=False)

#tạo class để trả về trang hỗ trợ      
class SupportView(View):
    def get(self, request):
        try:
            return render(request, 'support.html')
        except TemplateDoesNotExist:
            return render(request, 'error.html', {'message': 'Support page not found'}, status=404)
        except Exception as e:
            return render(request, 'error.html', {'message': str(e)}, status=500)

#tạo class để trả về trang hướng dẫn mua sắm   
class ShoppingGuideView(View):
    def get(self, request):
        try:
            return render(request, 'shopping_guide.html')
        except TemplateDoesNotExist:
            return render(request, 'error.html', {'message': 'ShoppingGuide page not found'}, status=404)
        except Exception as e:
            return render(request, 'error.html', {'message': str(e)}, status=500)
        
#tạo class để trả về trang chính sách đổi trả   
class ReturnPolicyView(View):
    def get(self, request):
        try:
            return render(request, 'return_policy.html')
        except TemplateDoesNotExist:
            return render(request, 'error.html', {'message': 'ReturnPolicy page not found'}, status=404)
        except Exception as e:
            return render(request, 'error.html', {'message': str(e)}, status=500)
        
#tạo class để trả về trang chính sách đổi trả   
class ShippingInforView(View):
    def get(self, request):
        try:
            return render(request, 'shipping_infor.html')
        except TemplateDoesNotExist:
            return render(request, 'error.html', {'message': 'ShippingInfor page not found'}, status=404)
        except Exception as e:
            return render(request, 'error.html', {'message': str(e)}, status=500)
        
#tạo class để trả về trang chính sách đổi trả   
class FAQsView(View):
    def get(self, request):
        try:
            return render(request, 'faqs.html')
        except TemplateDoesNotExist:
            return render(request, 'error.html', {'message': 'FAQs page not found'}, status=404)
        except Exception as e:
            return render(request, 'error.html', {'message': str(e)}, status=500)