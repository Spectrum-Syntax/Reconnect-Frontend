from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from reconnect.models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ("enrollment_number", "username", "role", "is_staff")
    search_fields = ("enrollment_number", "username")

    fieldsets = UserAdmin.fieldsets + (
        ("Custom Fields", {"fields": ("enrollment_number", "role")}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Custom Fields", {"fields": ("enrollment_number", "role")}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
