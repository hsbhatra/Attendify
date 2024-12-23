"""
URL configuration for FaceTrack project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('RegAndAuth.urls')),
    path("", include('attendance.urls')),
    path("", include('UserProfile.urls')),
    path("", include('LeaveApp.urls')),

    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("services/", views.services, name="services"),
    
    # admin urls
    path("dashboard/", views.dashboard, name="dashboard"),
    path("take_attendance/", views.take_attendance, name="take_attendance"),
    path("leave_application_records/", views.leave_application_records, name="leave_application_records"),
]
