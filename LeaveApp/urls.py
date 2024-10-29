from django.urls import path
from .views import apply_for_leave

urlpatterns = [
    path('leave-application-form/', apply_for_leave, name="apply_for_leave"),
]