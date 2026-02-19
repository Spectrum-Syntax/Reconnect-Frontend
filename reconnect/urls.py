from django.contrib import admin
from django.urls import path
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
]