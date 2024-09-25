from django.urls import path
from . import views

urlpatterns = [
    path("mark_attendance/", views.mark_attendance, name="mark_attendance"),
    path("check_your_attendance/", views.check_your_attendance, name="check_your_attendance"),
    path("complete_attendance_records/", views.complete_attendance_records, name="complete_attendance_records"),
    path("search_by_username/", views.search_by_username, name="search_by_username"),
    path("search_by_date/", views.search_by_date, name="search_by_date"),
]
