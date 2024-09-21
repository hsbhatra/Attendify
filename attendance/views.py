from django.shortcuts import render, redirect
# import datetime as dt
from django.utils import timezone
import qrcode
import base64
from io import BytesIO
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



