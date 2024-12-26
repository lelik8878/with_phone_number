from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from main.models import User


class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = (
        (None, {'fields': ('phone_number', 'nickname', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone_number", "usable_password", "password1", "password2"),
            },
        ),
    )
    list_display = ("phone_number", "nickname", "is_active", "is_staff")
    search_fields = ("phone_number", "nickname")
    ordering = ("phone_number", "nickname")


admin.site.register(User, CustomUserAdmin)

