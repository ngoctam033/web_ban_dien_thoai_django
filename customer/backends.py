from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

#tạo class để xác thực email và password

class EmailBackend(ModelBackend):
    def authenticate(self, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=kwargs['email'])
        except UserModel.DoesNotExist:
            return None

        if user.check_password(kwargs['password']):
            return user

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None