from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from reconnect.models import CustomUser, Event, EventTimelineItem, Announcement


class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ("enrollment_number", "username", "role", "department", "passed_out_year", "is_staff")
    search_fields = ("enrollment_number", "username", "first_name", "last_name", "department")
    list_filter = ("role", "department", "passed_out_year")

    fieldsets = UserAdmin.fieldsets + (
        ("Custom Fields", {"fields": ("enrollment_number", "role")}),
        ("Profile Info", {"fields": (
            "department", "passed_out_year", "cgpa", "working_status",
            "phone", "date_of_birth", "register_number", "profile_picture",
        )}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Custom Fields", {"fields": ("enrollment_number", "role")}),
        ("Profile Info", {"fields": (
            "department", "passed_out_year", "cgpa", "working_status",
            "phone", "date_of_birth", "register_number", "profile_picture",
        )}),
    )


class EventTimelineInline(admin.TabularInline):
    model = EventTimelineItem
    extra = 1


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_display', 'category', 'is_active', 'created_at')
    list_filter = ('category', 'is_active')
    search_fields = ('title', 'description')
    inlines = [EventTimelineInline]


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'importance', 'display_day', 'display_month', 'is_active', 'created_at')
    list_filter = ('importance', 'is_active')
    search_fields = ('title', 'body')


admin.site.register(CustomUser, CustomUserAdmin)
