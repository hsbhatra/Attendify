from django.shortcuts import redirect, render
import cv2
from pyzbar.pyzbar import decode
import numpy as np
import time
import datetime as dt
from attendance.models import Attendance
from django.contrib.auth.models import User
from django.utils import timezone

# =======================================================================================
# General views
# =======================================================================================

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

# =======================================================================================
# Admin views
# =======================================================================================

def dashboard(request):
    return render(request, 'admin/admin_dashboard.html')

def take_attendance(request): 
    # Open webcam
    cap = cv2.VideoCapture(0)
    
    time_between_logs_th = 3000  # Time threshold in seconds to prevent duplicate entries

    while True:
        ret, frame = cap.read()
        qr_info = decode(frame)  # Decode QR code from frame

        if len(qr_info) > 0:
            qr = qr_info[0]
            data = qr.data.decode()  # Decode the QR data
            rect = qr.rect

            username = data.split()[0].strip(',')
            qr_generation_time = data.split(',')[-1].strip()

            try:
                # Check if user exists in Django's default User model
                user = User.objects.get(username=username)

                # Display "Access Granted" on the screen
                cv2.putText(frame, 'ACCESS GRANTED', (rect.left, rect.top-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

                # Check the most recent attendance record in the database
                last_attendance = Attendance.objects.filter(user=user).order_by('-timestamp').first()

                # If there's no previous attendance or enough time has passed since the last one
                if not last_attendance or (timezone.now() - last_attendance.timestamp).total_seconds() > time_between_logs_th:
                    # Mark the attendance in the database
                    Attendance.objects.create(user=user, status='present')

            except User.DoesNotExist:
                # If user doesn't exist, display "Access Denied"
                cv2.putText(frame, 'ACCESS DENIED', (rect.left, rect.top-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

            # Draw rectangle around the QR code
            frame = cv2.rectangle(frame, (rect.left, rect.top), (rect.left + rect.width, rect.top + rect.height), (0, 255, 0), 5)
    
        # Display the frame
        cv2.imshow('webcam', frame)
    
        # Exit the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    return redirect('dashboard')

def leave_application_records(request):
    return render(request, "LeaveApp/leave_application_records.html")