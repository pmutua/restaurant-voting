from django.urls import path
from .views import *

app_name = 'api'


urlpatterns = [
    path('register_user/',   RegisterUserAPIView.as_view(), name="register-user"),
    path('user_login/', UserLoginAPIView.as_view(), name="user-login"),
    path('create_restaurant/', CreateRestaurantAPIView.as_view(), name="create-restaurant"),
    path('upload_menu/', UploadMenuAPIView.as_view(), name="upload-menu"),  
    
    
]

