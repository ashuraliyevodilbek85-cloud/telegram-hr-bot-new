from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.config import POSITIONS, EDUCATION_LEVELS, GENDERS, LANGUAGE_LEVELS, SUPPORTED_LANGUAGES


def get_position_keyboard(department_key: str):
    """Position selection keyboard (INLINE buttons only) based on department"""
    positions = POSITIONS.get(department_key, [])
    buttons = []
    for pos in positions:
        buttons.append([InlineKeyboardButton(text=pos, callback_data=f"position:{pos}")])
    
    # Add back button
    buttons.append([InlineKeyboardButton(text="⬅️ Orqaga", callback_data="position:back")])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_education_keyboard():
    """Education level keyboard (inline)"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=level, callback_data=f"education:{level}")]
            for level in EDUCATION_LEVELS
        ]
    )
    return keyboard


def get_gender_keyboard():
    """Gender selection keyboard (inline)"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=gender, callback_data=f"gender:{gender}")]
            for gender in GENDERS
        ]
    )
    return keyboard


def get_language_level_keyboard(language: str):
    """Language level keyboard (Russian or English) - inline"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=level, callback_data=f"{language}_level:{level}")]
            for level in LANGUAGE_LEVELS
        ]
    )
    return keyboard


def get_confirmation_keyboard():
    """Final confirmation keyboard (inline)"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Tasdiqlash", callback_data="confirm:yes"),
                InlineKeyboardButton(text="Orqaga", callback_data="confirm:back")
            ]
        ]
    )
    return keyboard


def get_skip_keyboard():
    """Skip button keyboard (inline)"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⏭️ O'tkazib yuborish", callback_data="skip")]
        ]
    )
    return keyboard


def get_language_selection_keyboard():
    """Language selection keyboard (inline)"""
    buttons = []
    for lang_code, lang_label in SUPPORTED_LANGUAGES.items():
        buttons.append([InlineKeyboardButton(text=lang_label, callback_data=f"lang:{lang_code}")])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_phone_confirmation_keyboard():
    """Phone number confirmation keyboard (inline)"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="phone_confirm:yes"),
                InlineKeyboardButton(text="✏️ O'zgartirish", callback_data="phone_confirm:edit")
            ]
        ]
    )
    return keyboard


def get_hr_decision_keyboard(user_id: int):
    """HR decision keyboard with approve/interview/reject buttons"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Qabul qilindi", callback_data=f"approve_{user_id}"),
                InlineKeyboardButton(text="🎤 Suhbatga chaqirish", callback_data=f"interview_{user_id}")
            ],
            [
                InlineKeyboardButton(text="❌ Rad etildi", callback_data=f"reject_{user_id}")
            ]
        ]
    )
    return keyboard