from django.urls import path
from .views import (get_main_page, user_registration, get_user_profile, get_login_page, log_out,
                    redirect_render,set_as_main_image, delete_image, delete_main_image)

urlpatterns = [
    path('', get_main_page, name='main_page'),
    path('user_registration/', user_registration, name='user_registration'),
    path('user_login/', get_login_page, name='login_page'),
    path('log_out/', log_out, name='log_out'),
    path('user_profile/<int:user_id>/', get_user_profile, name='user_profile'),
    path('redirect_render/', redirect_render, name='redirect_render'),
    path('set_as_main_image/', set_as_main_image, name='set_as_main_image'),
    path('delete_image/', delete_image, name='delete_image'),
    path('delete_main_image/', delete_main_image, name='delete_main_image'),
]