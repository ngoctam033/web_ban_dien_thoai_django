from django.db import models

class Contact(models.Model):
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=11)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()

    class Meta:
        db_table = "contact"
        
    def __str__(self):
        return self.email