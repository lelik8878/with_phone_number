from django.urls import path
from .views import get_main_page, user_registration, get_user_profile, get_login_page, log_out, redirect_render

urlpatterns = [
    path('', get_main_page, name='main_page'),
    path('user_registration/', user_registration, name='user_registration'),
    path('user_login/', get_login_page, name='login_page'),
    path('log_out/', log_out, name='log_out'),
    path('user_profile/<int:user_id>/', get_user_profile, name='user_profile'),
    path('redirect_render/', redirect_render, name='redirect_render'),
]