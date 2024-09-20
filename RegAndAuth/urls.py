from django.urls import path, include
from . import views

urlpatterns = [
    path("register/", views.register, name='register'),
    path("verify_otp/", views.verify_otp, name='verify_otp'),
    path("login/", views.login, name='login'),
    path("logout/", views.logout, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-reset-otp/', views.verify_reset_otp, name='verify_reset_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),

]