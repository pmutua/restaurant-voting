from django.urls import path
from .views import *

app_name = 'api'


urlpatterns = [
    path('register_user/', RegisterUserAPIView.as_view(), name="register-user"),
    path('login/', UserLoginAPIView.as_view(), name="user-login"),
    path('logout/', UserLogoutView.as_view(), name="user-logout"),
    path('create_restaurant/', CreateRestaurantAPIView.as_view(), name="create-restaurant"),
    path('upload_menu/', UploadMenuAPIView.as_view(), name="upload-menu"),
    path('create_employee/', CreateEmployeeAPIView.as_view(), name="create-employee"),
    path('restaurants/', RestaurantListAPIView.as_view(), name="restaurants"),
    path('menu_list/', CurrentDayMenuList.as_view(), name="menu-list"),
    path('vote/<int:menu_id>/', VoteAPIView.as_view(), name="new-vote"),
    path('results/', ResultsAPIView.as_view(), name="results"),

    






]
