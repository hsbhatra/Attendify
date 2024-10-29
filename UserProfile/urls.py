from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("all-users/", views.all_users, name="all_users"),
    path("profile/<str:pk>/", views.user_profile, name="profile"),
    
    path('upload-profile-picture/', views.upload_profile_picture, name='upload_profile_picture'),
    path("update-bio/", views.update_bio, name="update_bio"),
    path("update-dob/", views.update_dob, name="update_dob"),
    path("update-phone/", views.update_phone, name="update_phone"),
    path("update-address/", views.update_address, name="update_address"),
]

# Add this only if you are in development (DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

