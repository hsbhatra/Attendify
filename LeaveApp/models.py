from django.db import models

class LeaveApplication(models.Model):
    LEAVE_TYPE_CHOICES = [
        ('casual', 'Casual Leave'),
        ('compensatory', 'Compensatory Leave'),
        ('emergency', 'Emergency Leave'),
        ('marriage', 'Marriage Leave'),
        ('maternity', 'Maternity Leave'),
        ('paternity', 'Paternity Leave'),
        ('sick', 'Sick Leave'),
        ('study', 'Study Leave'),
        ('unpaid', 'Unpaid Leave'),
    ]

    leave_type = models.CharField(max_length=50, choices=LEAVE_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.leave_type} from {self.start_date} to {self.end_date}"

class Attachment(models.Model):
    leave_application = models.ForeignKey(LeaveApplication, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to='attachments/')

    def __str__(self):
        return self.file.name
