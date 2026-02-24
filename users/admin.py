from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from reconnect.models import (
    CustomUser, Event, EventTimelineItem, Announcement,
    Post, PostLike, PostComment, Connection, Opportunity, Project,
    Conversation, ConversationParticipant, Message,
)


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


# ─── Post / Social ──────────────────────────────────────────────────────────

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'post_type', 'content_preview', 'created_at')
    list_filter = ('post_type', 'created_at')
    search_fields = ('content', 'author__username')

    def content_preview(self, obj):
        return obj.content[:80] + '...' if len(obj.content) > 80 else obj.content
    content_preview.short_description = 'Content'


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'content_preview', 'created_at')
    search_fields = ('content', 'user__username')

    def content_preview(self, obj):
        return obj.content[:60] + '...' if len(obj.content) > 60 else obj.content
    content_preview.short_description = 'Content'


admin.site.register(PostLike)


# ─── Connection ──────────────────────────────────────────────────────────────

@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('from_user__username', 'to_user__username')


# ─── Opportunity & Project ───────────────────────────────────────────────────

@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'opportunity_type', 'location', 'is_active', 'created_at')
    list_filter = ('opportunity_type', 'is_active')
    search_fields = ('title', 'company', 'description')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'posted_by', 'is_active', 'created_at')
    list_filter = ('category', 'is_active')
    search_fields = ('title', 'description', 'tech_stack')


# ─── Chat / Messaging ───────────────────────────────────────────────────────

class ConversationParticipantInline(admin.TabularInline):
    model = ConversationParticipant
    extra = 1


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_group', 'created_at')
    list_filter = ('is_group',)
    search_fields = ('name',)
    inlines = [ConversationParticipantInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'sender', 'content_preview', 'timestamp')
    search_fields = ('content', 'sender__username')

    def content_preview(self, obj):
        return obj.content[:60] + '...' if len(obj.content) > 60 else obj.content
    content_preview.short_description = 'Content'
