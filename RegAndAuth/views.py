import random
from django.core.cache import cache
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from email.message import EmailMessage
import ssl
import smtplib
# Import email utility
from Utils.email_utils import send_email
from django.conf import settings
from UserProfile.models import UserProfile
# Import utility functions
from Utils.validation_utils import is_validate_password, is_validate_email, is_validate_username, validate_name
from Utils.security_utils import generate_secure_qr_data, validate_qr_data

# Create your views here.
def register(request):
    # Handles user registration and sends OTP for email verification
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        conf_password = request.POST['conf-password']

        if password == conf_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already used. Can't register again using the same username.")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email already used. Can't register again using the same email.")
                return redirect('register')
            elif validate_name(fname) is False:
                messages.error(request, "First name must contain alphabets (a-z, A-Z), spaces ( ), or hyphen (-), and must be between 2-50 in length.")
                return redirect('register')
            elif validate_name(lname) is False:
                messages.error(request, "Last name must contain alphabets (a-z, A-Z), spaces ( ), or hyphen (-), and must be between 2-50 in length.")
                return redirect('register')
            elif is_validate_username(username) is False:
                messages.error(request, "Username may contain uppercase character (A-Z), lowercase character (a-z), number (0-9), an optional underscore (_) as a special character, and It cannot contain spaces.")
                return redirect('register')
            elif is_validate_email(email) is False:
                messages.error(request, "Invalid Email Format.")
                return redirect('register')
            elif is_validate_password(password) is False:
                messages.error(request, "Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one number, and one special character (!@#$*^~?).")
                return redirect('register')
            else:
                # Generate a random 6-digit OTP
                otp = str(random.randint(100000, 999999))
                
                # Store the OTP in Django's cache with a timeout (e.g., 5 minutes)
                cache.set(email, otp, timeout=300)
                
                # Send the OTP to the user's email
                subject = "Your OTP for Email Verification"
                body = f"Your OTP for verifying your email is {otp}. It is valid for 5 minutes."
                sender_email = settings.EMAIL_HOST_USER
                sender_email_pass = settings.EMAIL_HOST_PASSWORD
                autoEmail(sender_email, sender_email_pass, email, subject, body)

                # Store user details temporarily in the session (without saving to the database yet)
                request.session['user_details'] = {
                    'first_name': fname,
                    'last_name': lname,
                    'username': username,
                    'email': email,
                    'password': password
                }

                # Redirect to the OTP verification page
                return redirect('verify_otp')
        else:
            messages.error(request, "Password doesn't match the Confirm Password.")
            return redirect('register')
    else:
        return render(request, 'RegAndAuth/register.html')
    
def verify_otp(request):
    # Verifies OTP sent to user's email and creates user account
    if request.method == "POST":
        entered_otp = request.POST['otp']
        email = request.session.get('user_details', {}).get('email')

        if email:
            # Get the OTP stored in cache
            stored_otp = cache.get(email)

            if entered_otp == stored_otp:
                # OTP matches; save the user
                user_details = request.session.pop('user_details')
                user = User.objects.create_user(
                    first_name=user_details['first_name'],
                    last_name=user_details['last_name'],
                    username=user_details['username'],
                    email=user_details['email'],
                    password=user_details['password']
                )
                user.save()
                profile = UserProfile.objects.create(user=user)
                profile.save()

                user = auth.authenticate(username=user.username, password=user_details['password'])
                if user is not None:
                    auth.login(request, user)
                    return redirect('index')
                else:
                    messages.error(request, "An unexpected error occurred during login. Please try logging in manually.")
                    return redirect('login')
            else:
                messages.error(request, "Invalid OTP. Please try again.")
                return redirect('verify_otp')
        else:
            messages.error(request, "Session expired. Please register again.")
            return redirect('register')
    else:
        return render(request, 'RegAndAuth/verify_otp.html')

def login(request):
    # Handles user login with username and password validation
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        if is_validate_username(username) is False:
            messages.error(request, "Username may contain uppercase character (A-Z), lowercase character (a-z), number (0-9), an optional underscore (_) as a special character, and It cannot contain spaces.")
            return redirect('login')
        elif is_validate_password(password) is False:
            messages.error(request, "Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one number, and one special character (!@#$*^~?).")
            return redirect('login')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid Credentials, try again!")
            return redirect('login')
            
    return render(request, 'RegAndAuth/login.html')

def forgot_password(request):
    # Initiates password reset by sending OTP to user's email
    if request.method == "POST":
        email = request.POST['email']
        
        if is_validate_email(email) is False:
            messages.error(request, "Invalid Email Format.")
            return redirect('forgot_password')
        
        if User.objects.filter(email=email).exists():
            # Generate a random 6-digit OTP
            otp = generate_otp()
            
            # Store the OTP in Django's cache with a timeout (e.g., 5 minutes)
            cache.set(email, otp, timeout=300)
            
            # Send the OTP to the user's email
            subject = "Your OTP for Password Reset"
            body = f"Your OTP for resetting your password is {otp}. It is valid for 5 minutes."
            sender_email = settings.EMAIL_HOST_USER
            sender_email_pass = settings.EMAIL_HOST_PASSWORD
            autoEmail(sender_email, sender_email_pass, email, subject, body)

            # Store the email temporarily in the session
            request.session['reset_email'] = email

            # Redirect to the OTP verification page
            return redirect('verify_reset_otp')
        else:
            messages.error(request, "Email not registered.")
            return redirect('forgot_password')
    else:
        return render(request, 'RegAndAuth/forgot_password.html')

def verify_reset_otp(request):
    # Verifies OTP for password reset process
    if request.method == "POST":
        entered_otp = request.POST['otp']
        email = request.session.get('reset_email')

        if email:
            # Get the OTP stored in cache
            stored_otp = cache.get(email)

            if entered_otp == stored_otp:
                # OTP matches; redirect to reset password form
                return redirect('reset_password')
            else:
                messages.error(request, "Invalid OTP. Please try again.")
                return redirect('verify_reset_otp')
        else:
            messages.error(request, "Session expired. Please try again.")
            return redirect('forgot_password')
    else:
        return render(request, 'RegAndAuth/verify_reset_otp.html')

def reset_password(request):
    # Resets user's password after OTP verification
    if request.method == "POST":
        password = request.POST['password']
        conf_password = request.POST['conf-password']
        email = request.session.get('reset_email')

        if email:
            if password == conf_password:
                if is_validate_password(password) is False:
                    messages.error(request, "Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one number, and one special character (!@#$*^~?).")
                    return redirect('reset_password')

                # Get the user object
                user = User.objects.get(email=email)
                
                # Set the new password
                user.set_password(password)
                user.save()

                # Clear the session data
                request.session.pop('reset_email')

                messages.success(request, "Password reset successfully. Please login.")
                return redirect('login')
            else:
                messages.error(request, "Password doesn't match the Confirm Password.")
                return redirect('reset_password')
        else:
            messages.error(request, "Session expired. Please try again.")
            return redirect('forgot_password')
    else:
        return render(request, 'RegAndAuth/reset_password.html')

def logout(request):
    # Logs out the current user
    # auth_logout(request)
    auth.logout(request)
    messages.info(request, "You are now logged-out successfuly!")
    return redirect('index')


def generate_otp():
    # Generates a random 6-digit OTP for verification
    return str(random.randint(100000, 999999))

def autoEmail(senderEmail, senderEmailPass, recieverEmail, subject, bodyOfEmail):
    # Utility wrapper for sending emails (OTP, notifications)
    return send_email(senderEmail, senderEmailPass, recieverEmail, subject, bodyOfEmail)