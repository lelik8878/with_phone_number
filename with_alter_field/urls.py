from django.urls import path
from .views import alter_field

urlpatterns = [
    path('', alter_field, name='alter_field'),
]
