from django.urls import path
from . import views

urlpatterns = [
    path("mark_attendance/", views.mark_attendance, name="mark_attendance"),
    path("check_your_attendance/", views.check_your_attendance, name="check_your_attendance"),
]
