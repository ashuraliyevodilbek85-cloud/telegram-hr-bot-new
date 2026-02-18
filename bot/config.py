import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# Resolve .env file path relative to project root (where run.py is located)
# This file is in bot/config.py, so we go up one level to reach project root
PROJECT_ROOT = Path(__file__).parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

# Load .env file explicitly, then fallback to OS environment variables
load_dotenv(dotenv_path=ENV_FILE, override=False)

logger = logging.getLogger(__name__)

# Bot configuration - try .env first, then OS environment as fallback
BOT_TOKEN = os.getenv("BOT_TOKEN")
# Telegram group ID where applications will be sent
# IMPORTANT: Must be int, not str (Telegram API requirement)
_hr_group_id_str = os.getenv("HR_GROUP_ID")
if _hr_group_id_str:
    try:
        HR_GROUP_ID = int(_hr_group_id_str)
    except (ValueError, TypeError):
        logger.error(
            f"Invalid HR_GROUP_ID value: {_hr_group_id_str}. " f"Must be an integer."
        )
        HR_GROUP_ID = None
else:
    HR_GROUP_ID = None

# Bot information
BOT_NAME = "Work at Proper"
COMPANY_NAME = "Proper English School"

# Languages
DEFAULT_LANGUAGE = "uz"
SUPPORTED_LANGUAGES = {"uz": "🇺🇿 O'zbek", "ru": "🇷🇺 Русский", "en": "🇬🇧 English"}

# Region (only Andijon)
REGION = "Andijon"

# Branches (Andijon only)
BRANCHES = {
    "clara": "Clara",
    "severniy": "Severniy",
    "business_center": "Business Center",
    "yangi_bozor": "Yangi Bozor",
}

# Departments with emojis
DEPARTMENTS = {
    "akademik": "🧠 Akademik bo'lim",
    "sotuv": "💼 Sotuv bo'limi",
    "smm": "📱 SMM bo'limi",
    "operational": "⚙️ Operational Team",
}

# Positions by department (exact as specified)
POSITIONS = {
    "akademik": [
        "SAT Teacher",
        "IELTS Instructor",
        "General English Teacher",
        "Kids English Teacher",
        "Assistant Teacher",
    ],
    "sotuv": ["Administrator", "Operator"],
    "smm": ["Brand Face", "Videographer / Editor"],
    "operational": [
        "Branch Manager",
        "HR",
        "Supervisor",
        "Marketing Manager",
        "SMM Manager",
        "Tozalik hodimasi",
    ],
}

# Education levels
EDUCATION_LEVELS = ["O'rta", "O'rta-maxsus", "Oliy"]

# Gender options
GENDERS = ["Erkak", "Ayol"]

# Language levels
LANGUAGE_LEVELS = ["Past", "O'rtacha", "Ilg'or"]

# Work experience options
WORK_EXPERIENCE = [
    "No experience",
    "1 year",
    "1-3 years",
    "3-5 years",
    "5+ years",
]

# Where did you hear about us options (will be text input)
# But we can provide common options as buttons if needed

# Minimum audio duration in seconds
MIN_AUDIO_DURATION = 10
