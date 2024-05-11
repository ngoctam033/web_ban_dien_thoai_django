from django.contrib import admin
from .models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone_number', 'email', 'subject', 'message')

admin.site.register(Contact, ContactAdmin)