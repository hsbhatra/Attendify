import re

PASSWORD_PATTERN = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$*^~?])[A-Za-z\d!@#$*^~?]{8,20}$')  # Password must be strong
EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(\.[a-zA-Z]{2,})?$')  # Valid email format
USERNAME_PATTERN = re.compile(r'^[A-Za-z0-9_]+$')  # Username rules
name_pattern = r"^[A-Za-z]+(?:[ -][A-Za-z]+)*$"  # Name validation

def is_validate_password(password):
    """Checks if password matches the required pattern"""
    return bool(PASSWORD_PATTERN.fullmatch(password))

def is_validate_email(email):
    """Checks if email is in valid format"""
    return bool(EMAIL_PATTERN.fullmatch(email))

def is_validate_username(username):
    """Checks if username matches allowed pattern"""
    return bool(USERNAME_PATTERN.fullmatch(username))

def validate_name(name):
    """Validates name for allowed characters and length"""
    if not name:
        return False
    return bool(re.match(name_pattern, name) and 2 <= len(name) <= 50)
