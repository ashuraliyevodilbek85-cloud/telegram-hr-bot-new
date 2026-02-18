from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot.config import BRANCHES, DEPARTMENTS, WORK_EXPERIENCE


def get_main_menu_keyboard():
    """Main menu keyboard (bottom only)"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🧳 Bo'sh ish o'rinlari")],
            [KeyboardButton(text="🏢 Kompaniya haqida")],
            [KeyboardButton(text="☎️ Kontaktlar")],
            [KeyboardButton(text="💬 Fikr-mulohazalar")],
            [KeyboardButton(text="🌐 Tilni o'zgartirish")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Tanlovni amalga oshiring"
    )
    return keyboard


def get_start_keyboard():
    """Start button keyboard"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="▶️ Start")]
        ],
        resize_keyboard=True
    )
    return keyboard


def get_branch_keyboard():
    """Branch selection keyboard (reply buttons)"""
    buttons = []
    for branch_name in BRANCHES.values():
        buttons.append([KeyboardButton(text=branch_name)])
    buttons.append([KeyboardButton(text="🔙 Orqaga")])
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
    return keyboard


def get_department_keyboard():
    """Department selection keyboard (reply buttons)"""
    buttons = []
    for dept_name in DEPARTMENTS.values():
        buttons.append([KeyboardButton(text=dept_name)])
    buttons.append([KeyboardButton(text="🔙 Orqaga")])
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
    return keyboard


def get_yes_no_keyboard():
    """Yes/No keyboard"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Ha"), KeyboardButton(text="Yo'q")],
            [KeyboardButton(text="🔙 Orqaga")]
        ],
        resize_keyboard=True
    )
    return keyboard


def get_back_keyboard():
    """Back button keyboard (for application flow - uses 🔙)"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔙 Orqaga")]
        ],
        resize_keyboard=True
    )
    return keyboard


def get_main_menu_back_keyboard():
    """Back button keyboard for main menu actions (uses ⬅️)"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⬅️ Orqaga")]
        ],
        resize_keyboard=True
    )
    return keyboard


def get_cancel_keyboard():
    """Cancel button keyboard"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="❌ Bekor qilish")]
        ],
        resize_keyboard=True
    )
    return keyboard


def get_work_experience_keyboard_reply():
    """Work experience keyboard (reply buttons)"""
    buttons = []
    for exp in WORK_EXPERIENCE:
        buttons.append([KeyboardButton(text=exp)])
    buttons.append([KeyboardButton(text="🔙 Orqaga")])
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
    return keyboard


def get_phone_keyboard():
    """Phone number input keyboard with contact button"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Kontaktni yuborish", request_contact=True)],
            [KeyboardButton(text="🔙 Orqaga")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Telefon raqami yoki kontakt"
    )
    return keyboard