from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    phone_prefix = models.CharField(max_length=3, null=True, blank=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    
    house_number = models.CharField(max_length=10, null=True, blank=True)
    street_name = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    postal_code = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} UserProfile'
