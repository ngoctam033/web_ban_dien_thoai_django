from django.contrib import messages
from django.shortcuts import redirect, render
from django.template import TemplateDoesNotExist
from django.views import View

from contact.models import Contact

class ContactView(View):
    def get(self, request):
        try:
            return render(request, 'contact.html')
        except TemplateDoesNotExist:
            return render(request, 'error.html', {'message': 'AboutUs page not found'}, status=404)
        except Exception as e:
            return render(request, 'error.html', {'message': str(e)}, status=500)

    def post(self, request):
        full_name = request.POST['ht']
        phone_number = request.POST['sdt']
        email = request.POST['em']
        subject = request.POST['tde']
        message = request.POST['nd']

        contact = Contact(full_name=full_name, phone_number=phone_number, email=email, subject=subject, message=message)
        contact.save()
        
        context = {
            'success_message': 'Thông tin đã được gửi thành công!'
        }

        return render(request, 'contact.html', context)
