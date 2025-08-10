# Attendify

Attendify is a Django-based attendance management system designed for schools, colleges, offices, and large organizations. It provides secure user authentication, QR code-based attendance marking, leave management, and admin reporting features.

## Features
- User registration with email OTP verification
- Login/logout and password reset
- User profile management
- QR code generation for attendance
- Lightning-fast QR code scanning
- Attendance tracking and reporting
- Real-time analytics and visualizations
- Smart dashboard for admins and users
- Leave management system with live status updates
- Bulk user import functionality
- Pagination, search, and filtering for user and leave records
- Recent activity feed for admins (user registration, attendance, leave applications)
- Role-based access and permissions (admin, user, etc.)
- Secure enterprise-grade encryption for user data
- Intuitive, user-friendly interface
- Enhanced mobile-friendly UI with smooth transitions and loading animations
- Privacy Policy, Terms of Service, and Cookie Policy pages
- Redis and Celery integration for background tasks
## Screenshots
Visual overview of Attendify features and UI:

| Home Page | Login | Sign Up |
|---|---|---|
| ![HomePage](Screen%20Shots/Full%20Page/HomePage.png) | ![LogIn](Screen%20Shots/Full%20Page/LogIn.png) | ![SignUp](Screen%20Shots/Full%20Page/SignUp.png) |

| User Profile | Dynamic QR Code | Valid QR Scan |
|---|---|---|
| ![UserProfile](Screen%20Shots/Full%20Page/UserProfile.png) | ![DynamicQrCode](Screen%20Shots/Full%20Page/DynamicQrCode.png) | ![ValidQr](Screen%20Shots/Full%20Page/ScanningQrForAttendance_ValidQr.png) |

| Invalid QR Scan | Leave Application | Attendance Records |
|---|---|---|
| ![InvalidQr](Screen%20Shots/Full%20Page/ScanningQrForAttendance_InvalidQr.png) | ![LeaveApp](Screen%20Shots/Full%20Page/LeaveApplicationForm.png) | ![AllAttendance](Screen%20Shots/Full%20Page/AllAttendanceRecords.png) |

| User Attendance | Services | About |
|---|---|---|
| ![UserAttendance](Screen%20Shots/Full%20Page/UserAttendanceRecords.png) | ![ServicePage](Screen%20Shots/Full%20Page/ServicePage.png) | ![AboutPage](Screen%20Shots/Full%20Page/AboutPage.png) |

## Getting Started

### Prerequisites
- Python 3.11+
- Redis (for OTP and Celery tasks)

### Installation
1. Clone the repository:
   ```sh
   git clone <repo-url>
   cd Attendify
   ```
2. Create and activate a virtual environment:
   ```sh
   python -m venv env
   env\Scripts\activate  # On Windows
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Set up environment variables in `.env` (see below).
5. Run migrations:
   ```sh
   python manage.py migrate
   ```
6. Create a superuser:
   ```sh
   python manage.py createsuperuser
   ```
7. Start the development server:
   ```sh
   python manage.py runserver
   ```

## Environment Variables
Create a `.env` file in the project root with the following keys:
```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=465
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
SECRET_KEY=your_django_secret_key
REDIS_URL=redis://localhost:6379/0
```

## Project Status
See `PROJECT_STATUS.md` for a detailed breakdown of completed, pending, and planned features.

## License
MIT
