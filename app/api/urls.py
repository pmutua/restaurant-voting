from django.urls import path
from .views import (
    RoleListAPIView,
    RegisterUserAPIView,
    UserLoginAPIView,
    UserLogoutView,
    CreateRestaurantAPIView,
    UploadMenuAPIView,
    CreateEmployeeAPIView,
    RestaurantListAPIView,
    CurrentDayMenuList,
    VoteAPIView,
    ResultsAPIView

)

app_name = 'api'


urlpatterns = [
    path(
        'roles/',
        RoleListAPIView.as_view(),
        name="roles"),
    path(
        'register_user/',
        RegisterUserAPIView.as_view(),
        name="register-user"),
    path(
        'login/',
        UserLoginAPIView.as_view(),
        name="login"),
    path(
        'logout/',
        UserLogoutView.as_view(),
        name="logout"),
    path(
        'create_restaurant/',
        CreateRestaurantAPIView.as_view(),
        name="create-restaurant"),
    path(
        'upload_menu/',
        UploadMenuAPIView.as_view(),
        name="upload-menu"),
    path(
        'create_employee/',
        CreateEmployeeAPIView.as_view(),
        name="create-employee"),
    path(
        'restaurants/',
        RestaurantListAPIView.as_view(),
        name="restaurants"),
    path(
        'menu_list/',
        CurrentDayMenuList.as_view(),
        name="menu-list"),
    path(
        'vote/<int:menu_id>/',
        VoteAPIView.as_view(),
        name="new-vote"),
    path(
        'results/',
        ResultsAPIView.as_view(),
        name="results"),
]
