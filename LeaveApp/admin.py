from django.contrib import admin
from .models import LeaveApplication, Attachment

# Register your models here.
admin.site.register(LeaveApplication)
admin.site.register(Attachment)