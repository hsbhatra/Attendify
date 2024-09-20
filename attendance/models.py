from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone  # Import timezone for timezone-aware conversion

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically records the time of attendance
    status = models.CharField(max_length=20, choices= [('Absent', 'Absent'), ('Present', 'Present')], default='Absent')

    def __str__(self):
        # Convert timestamp to the local timezone (Indian Standard Time)
        local_timestamp = timezone.localtime(self.timestamp)
        return f'{self.user.username} - {self.status} - {local_timestamp.strftime("%Y-%m-%d %H:%M:%S")}'