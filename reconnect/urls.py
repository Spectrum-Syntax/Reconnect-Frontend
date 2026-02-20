from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('alumni-dashboard/', views.alumni_dashboard, name='alumni_dashboard'),

    path('events/', views.events, name='events'),
    path('announcements/', views.announcements, name='announcements'),
    path('connect/', views.connect, name='connect'),
    path('settings/', views.settings_view, name='settings'),
    path('profile/', views.profile, name='profile'),
    path('event-details/', views.event_details, name='event_details'),

    # ── Admin API ─────────────────────────────────────────────────────────
    path('api/bulk-upload/', views.bulk_upload_users, name='bulk_upload'),
    path('api/create-user/', views.create_single_user, name='create_user'),

    # ── Profile / Settings API ────────────────────────────────────────────
    path('api/profile/update/', views.update_profile, name='update_profile'),

    # ── Chat API ──────────────────────────────────────────────────────────
    path('api/conversations/', views.conversation_list, name='conversation_list'),
    path('api/conversations/create/', views.conversation_create, name='conversation_create'),
    path('api/conversations/<str:conversation_id>/messages/', views.conversation_messages, name='conversation_messages'),
    path('api/users/search/', views.user_search, name='user_search'),

    # ── Events & Announcements API ────────────────────────────────────────
    path('api/events/', views.api_events_list, name='api_events_list'),
    path('api/events/create/', views.create_event, name='create_event'),
    path('api/events/<int:event_id>/delete/', views.delete_event, name='delete_event'),
    path('api/announcements/', views.api_announcements_list, name='api_announcements_list'),
    path('api/announcements/create/', views.create_announcement, name='create_announcement'),
    path('api/announcements/<int:announcement_id>/delete/', views.delete_announcement, name='delete_announcement'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)