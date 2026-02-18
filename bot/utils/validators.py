import re
from datetime import datetime

# Valid Uzbekistan operator codes (first 2 digits after +998)
VALID_OPERATORS = {
    '90', '91', '92', '93', '94', '95', '97', '98', '99',  # Ucell, Beeline, UMS, etc.
    '88', '89',  # Alternative codes
    '50', '51', '55', '60', '61', '62', '65', '66', '67', '68', '69',  # Mobile operators
    '71', '72', '73', '74', '75', '76', '77', '78', '79'  # Additional codes
}


def validate_phone(phone: str) -> bool:
    """
    Strict validation for Uzbekistan phone numbers.
    Format: +998XXXXXXXXX (exactly 12 digits total)
    
    Validates:
    - Exact format: +998 followed by 9 digits
    - Country code: +998
    - Operator code: First 2 digits after country code must be valid
    - Total length: Exactly 12 characters (+998XXXXXXXXX)
    - Rejects all-zero numbers and obviously invalid patterns
    """
    if not phone or not isinstance(phone, str):
        return False
    
    # Remove any whitespace
    phone = phone.strip()
    
    # Must start with +998
    if not phone.startswith('+998'):
        return False
    
    # Check exact format: +998 followed by exactly 9 digits
    pattern = r'^\+998\d{9}$'
    if not re.match(pattern, phone):
        return False
    
    # Extract operator code (first 2 digits after +998)
    operator_code = phone[4:6]
    
    # Validate operator code
    if operator_code not in VALID_OPERATORS:
        return False
    
    # Additional check: all digits must be numeric (already checked by regex, but double-check)
    digits = phone[4:]  # All digits after +998
    if not digits.isdigit() or len(digits) != 9:
        return False
    
    # Reject all-zero numbers (obviously invalid)
    if digits == '000000000':
        return False
    
    # Reject patterns that are too repetitive (likely invalid)
    if len(set(digits)) < 3:  # At least 3 different digits
        # Allow operator code repetition, but check last 7 digits
        last_seven = digits[2:]
        if len(set(last_seven)) < 2:  # Last 7 digits should have at least 2 different digits
            return False
    
    return True


def validate_date(date_str: str) -> bool:
    """Validate date format: DD.MM.YYYY"""
    try:
        datetime.strptime(date_str, "%d.%m.%Y")
        return True
    except ValueError:
        return False


def format_phone(phone: str) -> str:
    """
    Format phone number to +998XXXXXXXXX.
    Handles various input formats and normalizes to standard format.
    
    Accepts:
    - +998901234567
    - 998901234567
    - 901234567
    - Spaces, dashes, parentheses are stripped
    
    Returns: +998XXXXXXXXX (normalized format)
    """
    if not phone or not isinstance(phone, str):
        return ''
    
    # Remove all non-digit characters except +
    cleaned = re.sub(r'[^\d+]', '', phone.strip())
    
    # Remove any + signs except at the beginning
    if '+' in cleaned:
        cleaned = '+' + cleaned.replace('+', '')
    
    # Handle different input formats
    if cleaned.startswith('+998'):
        # Already in correct format, just ensure 9 digits after +998
        digits = cleaned[4:]
        if len(digits) == 9 and digits.isdigit():
            return cleaned
        # If wrong length, try to fix
        if digits.isdigit() and len(digits) >= 9:
            return '+998' + digits[:9]
    
    elif cleaned.startswith('998'):
        # Missing + prefix
        digits = cleaned[3:]
        if len(digits) == 9 and digits.isdigit():
            return '+' + cleaned
        # If wrong length, try to fix
        if digits.isdigit() and len(digits) >= 9:
            return '+998' + digits[:9]
    
    elif cleaned.startswith('9'):
        # Missing country code
        if len(cleaned) == 9 and cleaned.isdigit():
            return '+998' + cleaned
        # If wrong length, try to fix
        if cleaned.isdigit() and len(cleaned) >= 9:
            return '+998' + cleaned[:9]
    
    else:
        # Try to extract 9 digits from end
        digits_only = re.sub(r'[^\d]', '', cleaned)
        if len(digits_only) >= 9:
            # Take last 9 digits
            return '+998' + digits_only[-9:]
    
    # If we can't format it, return empty string (will be rejected by validation)
    return ''
