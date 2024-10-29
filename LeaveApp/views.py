from django.shortcuts import redirect, render
from .models import LeaveApplication

# Create your views here.

def apply_for_leave(request):
    if request.method == 'POST':
        leave_type = request.POST.get('leave_type')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        description = request.POST.get('description')
        attachments = request.FILES.getlist('attachments')  # Use getlist for multiple file uploads

        # Create a new LeaveApplication instance
        leave_application = LeaveApplication(
            leave_type=leave_type,
            start_date=start_date,
            end_date=end_date,
            description=description,
        )
        leave_application.save()

        # Save the attachments
        for attachment in attachments:
            leave_application.attachments.create(file=attachment)
       
        # leave_application.attachments.save()

        return redirect('index')
    
    return render(request, 'LeaveApp/leave_application_form.html')