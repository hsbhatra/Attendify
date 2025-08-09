# Attendify

Attendify is a Django-based attendance management system designed for schools, colleges, offices, and large organizations. It provides secure user authentication, QR code-based attendance marking, leave management, and admin reporting features.

## Features
- User registration with email OTP verification
- Login/logout and password reset
- User profile management
- QR code generation for attendance
- Attendance tracking and reporting
- Leave management system
- Admin panel for user and attendance management
- Redis and Celery integration for background tasks

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
