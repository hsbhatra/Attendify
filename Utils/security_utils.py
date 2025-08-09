import hashlib
import time
from django.conf import settings

def generate_secure_qr_data(user_id):
    """
    Generates secure QR code data for attendance marking.
    Includes user_id, current timestamp, and a hash for validation.
    """
    timestamp = int(time.time())
    secret = settings.SECRET_KEY
    raw = f"{user_id}:{timestamp}:{secret}"
    qr_hash = hashlib.sha256(raw.encode()).hexdigest()
    return f"{user_id}|{timestamp}|{qr_hash}"

def validate_qr_data(qr_data, max_age=120):
    """
    Validates QR code data for attendance.
    Checks hash and ensures QR code is not expired (default 2 minutes).
    Returns (is_valid, user_id) tuple.
    """
    try:
        user_id, timestamp, qr_hash = qr_data.split('|')
        timestamp = int(timestamp)
        now = int(time.time())
        if now - timestamp > max_age:
            return (False, None)
        secret = settings.SECRET_KEY
        raw = f"{user_id}:{timestamp}:{secret}"
        expected_hash = hashlib.sha256(raw.encode()).hexdigest()
        if qr_hash == expected_hash:
            return (True, user_id)
        else:
            return (False, None)
    except Exception:
        return (False, None)
