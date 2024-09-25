from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.contrib.auth.models import User
import qrcode
import base64
from io import BytesIO
from datetime import datetime, timedelta
from django.db.models import Q
from .models import Attendance

# Create your views here.

# Mark Attendance
def mark_attendance(request):
    if request.user.is_authenticated:
        user = request.user
        now = timezone.now()  # Use timezone-aware datetime

        # Format date and time to match the expected format
        formatted_date = now.strftime("%A, %B %d, %Y")
        formatted_time = now.strftime("%I:%M:%S %p")
        
        # Combine date and time for QR code
        qr_data = f"{user.username}, {formatted_date}, {formatted_time}"
        print(qr_data)
        qr_img = generate_qr_code(qr_data)

        # Convert image to base64
        img_str = convert_to_base64(qr_img)

        # Return the QR code on the web page
        return render(request, "attendance/mark_attendance.html", {'qr_code': img_str})

def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

def convert_to_base64(img):
    buffer = BytesIO()
    img = img.convert("RGB")
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode()

# Check Attendance
def check_your_attendance(request):
    if request.user.is_authenticated:
        # Fetch attendance records for the currently logged-in user
        attendance_records = Attendance.objects.filter(user=request.user)
        return render(request, 'attendance/check_your_attendance.html', {'attendance_records': attendance_records})
    else:
        return redirect('login')

def complete_attendance_records(request):
    if request.user.is_authenticated and request.user.is_superuser:
        complete_attendance_records = reversed(list(Attendance.objects.all()))
    return render(request, 'attendance/complete_attendance_records.html', {'complete_attendance_records': complete_attendance_records})

def search_by_username(request):
    filtered_attendance_records = []

    if request.method == "POST":
        username = request.POST.get('search_by_username', '').strip()

        # Check if username exists and filter attendance records accordingly
        try:
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
                filtered_attendance_records = reversed(Attendance.objects.filter(user=user))
            else:
                print(f"User with username '{username}' does not exist.")
        except User.DoesNotExist:
            print(f"User with username '{username}' not found.")
        
        # Debugging output
        print(f"Filtered records for username '{username}': {filtered_attendance_records}")
    
    return render(request, 'attendance/search_by_username.html', {'filtered_attendance_records': filtered_attendance_records})

def search_by_date(request):
    if request.method == 'POST':
        # Get the start and end dates from the form
        start_date_str = request.POST['start_date']
        end_date_str = request.POST['end_date']

        try:
            # Convert the start and end date strings into date objects
            start_date = parse_date(start_date_str)
            end_date = parse_date(end_date_str)

            if start_date and end_date:
                # Adjust the start_date to the beginning of the day (00:00:00)
                start_datetime = datetime.combine(start_date, datetime.min.time())

                # Adjust the end_date to the end of the day (23:59:59)
                end_datetime = datetime.combine(end_date, datetime.max.time())

                # Filter attendance records where the timestamp is between start_date and end_date
                filtered_attendance_records = Attendance.objects.filter(
                    timestamp__range=[start_datetime, end_datetime]
                )
            else:
                filtered_attendance_records = []

        except Exception as e:
            # If there's an issue (e.g. date parsing), return an empty list
            filtered_attendance_records = []

        return render(request, 'attendance/search_by_date.html', {
            'filtered_attendance_records': filtered_attendance_records,
            'start_date': start_date_str,
            'end_date': end_date_str
        })

    return render(request, 'attendance/search_by_date.html', {'filtered_attendance_records': []})