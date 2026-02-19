from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, "home.html")


def login_view(request):
    if request.method == "POST":
        enrollment = request.POST.get("enrollment_number")  # changed
        password = request.POST.get("password")

        # still pass as username (Django expects this key)
        user = authenticate(request, username=enrollment, password=password)

        if user is not None:
            login(request, user)

            # Role-based redirect
            if user.role == "admin":
                return redirect("admin_dashboard")

            elif user.role == "student":
                return redirect("student_dashboard")

            elif user.role == "alumni":
                return redirect("alumni_dashboard")

        else:
            messages.error(request, "Invalid enrollment number or password")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def admin_dashboard(request):
    return render(request, "admin.html")


@login_required
def student_dashboard(request):
    return render(request, "student/studentdash.html")


@login_required
def alumni_dashboard(request):
    return render(request, "alumini/aluminidash.html")


@login_required
def events(request):
    return render(request, "alumini/events.html")


@login_required
def announcements(request):
    return render(request, "alumini/announcements.html")


@login_required
def connect(request):
    return render(request, "alumini/connect.html")


@login_required
def settings_view(request):
    return render(request, "alumini/settings.html")


@login_required
def profile(request):
    return render(request, "alumini/profile.html")


@login_required
def event_details(request):
    return render(request, "alumini/eventdetails.html")