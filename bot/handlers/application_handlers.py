"""Application handlers - Step-by-step FSM flow"""
import logging
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from datetime import datetime

from bot.states.application_states import ApplicationStates
from bot.keyboards.reply_keyboards import (
    get_branch_keyboard, get_department_keyboard, get_main_menu_keyboard,
    get_yes_no_keyboard, get_back_keyboard, get_work_experience_keyboard_reply,
    get_phone_keyboard
)
from bot.keyboards.inline_keyboards import (
    get_position_keyboard, get_education_keyboard, get_gender_keyboard,
    get_language_level_keyboard, get_confirmation_keyboard, get_skip_keyboard,
    get_phone_confirmation_keyboard, get_hr_decision_keyboard
)
from bot.config import (
    BRANCHES, DEPARTMENTS, POSITIONS, HR_GROUP_ID, MIN_AUDIO_DURATION,
    COMPANY_NAME, REGION
)
from bot.utils.validators import validate_phone, validate_date, format_phone
from bot.utils.formatters import format_application_summary
from bot.utils.file_handlers import send_media_to_group
from bot.utils.texts import get_text

logger = logging.getLogger(__name__)
router = Router()


# ============================================
# STEP 1: VACANCY SELECTION
# ============================================

@router.message(ApplicationStates.waiting_for_branch)
async def process_branch(message: Message, state: FSMContext):
    """Process branch selection (REPLY BUTTONS)"""
    # Get user language from state
    data = await state.get_data()
    user_lang = data.get("user_language", "uz")
    
    if message.text == "🔙 Orqaga":
        # Preserve user language and return to main menu
        await state.clear()
        await state.update_data(user_language=user_lang)
        await message.answer(
            get_text("main_menu", lang=user_lang) + ":",
            reply_markup=get_main_menu_keyboard()
        )
        return
    
    # Check if selected branch is valid
    branch_name = None
    for key, name in BRANCHES.items():
        if message.text == name:
            branch_name = name
            break
    
    if not branch_name:
        error_text = get_text("invalid_selection", lang=user_lang)
        if error_text == "invalid_selection":
            error_text = "❌ Iltimos, tugmalardan birini tanlang:"
        await message.answer(error_text)
        return
    
    # Update state with branch selection, preserve language
    await state.update_data(branch=branch_name, city=REGION, user_language=user_lang)
    confirmation_text = get_text("branch_selected", lang=user_lang)
    if confirmation_text == "branch_selected":
        confirmation_text = f"✅ Filial: {branch_name}\n\n📋 Endi bo'limni tanlang:"
    await message.answer(confirmation_text)
    await message.answer(get_text("select_department", lang=user_lang), reply_markup=get_department_keyboard())
    await state.set_state(ApplicationStates.waiting_for_department)


@router.message(ApplicationStates.waiting_for_department)
async def process_department(message: Message, state: FSMContext):
    """Process department selection (REPLY BUTTONS)"""
    # Get user language from state
    data = await state.get_data()
    user_lang = data.get("user_language", "uz")
    
    if message.text == "🔙 Orqaga":
        await message.answer(get_text("select_branch", lang=user_lang), reply_markup=get_branch_keyboard())
        await state.set_state(ApplicationStates.waiting_for_branch)
        return
    
    # Check if selected department is valid
    dept_key = None
    dept_name = None
    for key, name in DEPARTMENTS.items():
        if message.text == name:
            dept_key = key
            dept_name = name
            break
    
    if not dept_key:
        error_text = get_text("invalid_selection", lang=user_lang)
        if error_text == "invalid_selection":
            error_text = "❌ Iltimos, tugmalardan birini tanlang:"
        await message.answer(error_text)
        return
    
    # Update state with department, preserve language
    await state.update_data(department=dept_name, department_key=dept_key, user_language=user_lang)
    confirmation_text = get_text("department_selected", lang=user_lang)
    if confirmation_text == "department_selected":
        confirmation_text = f"✅ Bo'lim: {dept_name}\n\n💼 Endi lavozimni tanlang (inline tugmalar):"
    await message.answer(confirmation_text)
    await message.answer(get_text("select_position", lang=user_lang), reply_markup=get_position_keyboard(dept_key))
    await state.set_state(ApplicationStates.waiting_for_position)


@router.callback_query(F.data.startswith("position:"), ApplicationStates.waiting_for_position)
async def process_position(callback: CallbackQuery, state: FSMContext):
    """Process position selection (INLINE BUTTONS)"""
    # Get user language from state
    data = await state.get_data()
    user_lang = data.get("user_language", "uz")
    
    position = callback.data.split(":", 1)[1]
    
    # Handle back button
    if position == "back":
        back_text = get_text("back", lang=user_lang)
        if back_text == "back":
            back_text = "Orqaga"
        await callback.answer(back_text)
        await callback.message.edit_text(get_text("select_department", lang=user_lang))
        await callback.message.answer(get_text("select_department", lang=user_lang), reply_markup=get_department_keyboard())
        await state.set_state(ApplicationStates.waiting_for_department)
        return
    
    # Update state with position, preserve language
    await state.update_data(position=position, user_language=user_lang)
    answer_text = get_text("position_selected", lang=user_lang)
    if answer_text == "position_selected":
        answer_text = f"Lavozim tanlandi: {position}"
    await callback.answer(answer_text)
    
    # Start personal information collection
    position_confirmation = get_text("position_confirmed", lang=user_lang)
    if position_confirmation == "position_confirmed":
        position_confirmation = f"✅ Lavozim: {position}"
    await callback.message.edit_text(position_confirmation)
    await callback.message.answer(get_text("personal_info", lang=user_lang))
    await callback.message.answer(get_text("ask_passport_name", lang=user_lang), reply_markup=get_back_keyboard())
    await state.set_state(ApplicationStates.waiting_for_passport_name)


@router.message(ApplicationStates.waiting_for_position)
async def process_position_text(message: Message, state: FSMContext):
    """Handle text messages during position selection (show keyboard again)"""
    # Get user language from state
    data = await state.get_data()
    user_lang = data.get("user_language", "uz")
    
    if message.text == "🔙 Orqaga":
        await message.answer(get_text("select_department", lang=user_lang), reply_markup=get_department_keyboard())
        await state.set_state(ApplicationStates.waiting_for_department)
        return
    
    dept_key = data.get("department_key")
    prompt_text = get_text("select_position_prompt", lang=user_lang)
    if prompt_text == "select_position_prompt":
        prompt_text = "Iltimos, lavozimni inline tugmalardan tanlang:"
    await message.answer(prompt_text, reply_markup=get_position_keyboard(dept_key))


# ============================================
# STEP 2: PERSONAL INFORMATION (ALL REQUIRED)
# ============================================

@router.message(ApplicationStates.waiting_for_passport_name)
async def process_passport_name(message: Message, state: FSMContext):
    """Process passport name"""
    # Get user language from state
    data = await state.get_data()
    user_lang = data.get("user_language", "uz")
    
    if message.text == "🔙 Orqaga":
        dept_key = data.get("department_key")
        position_prompt = get_text("select_position", lang=user_lang)
        await message.answer(position_prompt, reply_markup=get_position_keyboard(dept_key))
        await state.set_state(ApplicationStates.waiting_for_position)
        return
    
    # Preserve language when updating data
    await state.update_data(passport_name=message.text, user_language=user_lang)
    await message.answer(get_text("ask_passport_surname", lang=user_lang), reply_markup=get_back_keyboard())
    await state.set_state(ApplicationStates.waiting_for_passport_surname)


@router.message(ApplicationStates.waiting_for_passport_surname)
async def process_passport_surname(message: Message, state: FSMContext):
    """Process passport surname"""
    # Get user language from state
    data = await state.get_data()
    user_lang = data.get("user_language", "uz")
    
    if message.text == "🔙 Orqaga":
        await message.answer(get_text("ask_passport_name", lang=user_lang), reply_markup=get_back_keyboard())
        await state.set_state(ApplicationStates.waiting_for_passport_name)
        return
    
    # Preserve language when updating data
    await state.update_data(passport_surname=message.text, user_language=user_lang)
    await message.answer(get_text("ask_father_name", lang=user_lang), reply_markup=get_back_keyboard())
    await state.set_state(ApplicationStates.waiting_for_father_name)


@router.message(ApplicationStates.waiting_for_father_name)
async def process_father_name(message: Message, state: FSMContext):
    """Process father's name"""
    # Get user language from state
    data = await state.get_data()
    user_lang = data.get("user_language", "uz")
    
    if message.text == "🔙 Orqaga":
        await message.answer(get_text("ask_passport_surname", lang=user_lang), reply_markup=get_back_keyboard())
        await state.set_state(ApplicationStates.waiting_for_passport_surname)
        return
    
    # Preserve language when updating data
    await state.update_data(father_name=message.text, user_language=user_lang)
    await message.answer(get_text("ask_date_of_birth", lang=user_lang), reply_markup=get_back_keyboard())
    await state.set_state(ApplicationStates.waiting_for_date_of_birth)


@router.message(ApplicationStates.waiting_for_date_of_birth)
async def process_date_of_birth(message: Message, state: FSMContext):
    """Process date of birth"""
    # Get user language from state
    data = await state.get_data()
    user_lang = data.get("user_language", "uz")
    
    if message.text == "🔙 Orqaga":
        await message.answer(get_text("ask_father_name", lang=user_lang), reply_markup=get_back_keyboard())
        await state.set_state(ApplicationStates.waiting_for_father_name)
        return
    
    if not validate_date(message.text):
        await message.answer(get_text("invalid_date", lang=user_lang))
        return
    
    # Preserve language when updating data
    await state.update_data(date_of_birth=message.text, user_language=user_lang)
    await message.answer(get_text("ask_address", lang=user_lang), reply_markup=get_back_keyboard())
    await state.set_state(ApplicationStates.waiting_for_address)


@router.message(ApplicationStates.waiting_for_address)
async def process_address(message: Message, state: FSMContext):
    """Process address"""
    # Get user language from state
    data = await state.get_data()
    user_lang = data.get("user_language", "uz")
    
    if message.text == "🔙 Orqaga":
        await message.answer(get_text("ask_date_of_birth", lang=user_lang), reply_markup=get_back_keyboard())
        await state.set_state(ApplicationStates.waiting_for_date_of_birth)
        return
    
    # Preserve language when updating data
    await state.update_data(address=message.text, user_language=user_lang)
    await message.answer(get_text("ask_phone", lang=user_lang), reply_markup=get_phone_keyboard())
    await state.set_state(ApplicationStates.waiting_for_phone)


@router.message(ApplicationStates.waiting_for_phone, F.contact)
async def process_phone_contact(message: Message, state: FSMContext):
    """Process phone number from contact sharing (PRIMARY METHOD)"""
    # Get user language from state
    data = await state.get_data()
    user_lang = data.get("user_language", "uz")
    
    # Extract phone from contact
    if not message.contact or not message.contact.phone_number:
        error_text = get_text("invalid_phone", lang=user_lang)
        await message.answer(error_text, reply_markup=get_phone_keyboard())
        return
    
    contact_phone = message.contact.phone_number
    
    # Format and validate
    formatted_phone = format_phone(contact_phone)
    if not validate_phone(formatted_phone):
        error_text = get_text("invalid_phone", lang=user_lang)
        await message.answer(error_text, reply_markup=get_phone_keyboard())
        return
    
    # Store phone temporarily (will be confirmed in next step)
    await state.update_data(phone=formatted_phone, user_language=user_lang)
    
    # Show confirmation step
    confirmation_text = get_text("phone_confirmation_question", lang=user_lang)
    if confirmation_text == "phone_confirmation_question":
        confirmation_text = "Telefon raqamingiz to'g'rimi?"
    
    phone_display = get_text("phone_formatted_display", lang=user_lang)
    if phone_display == "phone_formatted_display":
        phone_display = "📱 Telefon raqami:"
    
    await message.answer(
        f"{phone_display}\n`{formatted_phone}`\n\n{confirmation_text}",
        parse_mode="Markdown",
        reply_markup=get_phone_confirmation_keyboard()
    )
    await state.set_state(ApplicationStates.waiting_for_phone_confirmation)


@router.message(ApplicationStates.waiting_for_phone)
async def process_phone(message: Message, state: FSMContext):
    """
    Process phone number from manual text input (SECONDARY METHOD).
    Only accepts if user types the number manually.
    """
    # Get user language from state
    data = await state.get_data()
    user_lang = data.get("user_language", "uz")
    
    # Handle back button
    if message.text == "🔙 Orqaga":
        await message.answer(get_text("ask_address", lang=user_lang), reply_markup=get_back_keyboard())
        await state.set_state(ApplicationStates.waiting_for_address)
        return
    
    # Reject contact button text if sent as text (not actual contact)
    if message.text and ("kontakt" in message.text.lower() or "contact" in message.text.lower()):
        error_text = get_text("invalid_phone", lang=user_lang)
        await message.answer(error_text, reply_markup=get_phone_keyboard())
        return
    
    # Reject empty or non-text input
    if not message.text or not message.text.strip():
        error_text = get_text("invalid_phone", lang=user_lang)
        await message.answer(error_text, reply_markup=get_phone_keyboard())
        return
    
    # Format the phone number
    formatted_phone = format_phone(message.text.strip())
    
    # Strict validation
    if not formatted_phone or not validate_phone(formatted_phone):
        error_text = get_text("invalid_phone", lang=user_lang)
        await message.answer(error_text, reply_markup=get_phone_keyboard())
        return
    
    # Store phone temporarily (will be confirmed in next step)
    await state.update_data(phone=formatted_phone, user_language=user_lang)
    
    # Show confirmation step
    confirmation_text = get_text("phone_confirmation_question", lang=user_lang)
    if confirmation_text == "phone_confirmation_question":
        confirmation_text = "Telefon raqamingiz to'g'rimi?"
    
    phone_display = get_text("phone_formatted_display", lang=user_lang)
    if phone_display == "phone_formatted_display":
        phone_display = "📱 Telefon raqami:"
    
    await message.answer(
        f"{phone_display}\n`{formatted_phone}`\n\n{confirmation_text}",
        parse_mode="Markdown",
        reply_markup=get_phone_confirmation_keyboard()
    )
    await state.set_state(ApplicationStates.waiting_for_phone_confirmation)


@router.callback_query(F.data.startswith("phone_confirm:"), ApplicationStates.waiting_for_phone_confirmation)
async def process_phone_confirmation(callback: CallbackQuery, state: FSMContext):
    """Process phone number confirmation"""
    # Get user language from state
    data = await state.get_data()
    user_lang = data.get("user_language", "uz")
    
    action = callback.data.split(":", 1)[1]
    
    if action == "yes":
        # Confirm - proceed to next step
        phone = data.get("phone")
        
        # Double-check phone is valid before proceeding
        if not phone or not validate_phone(phone):
            error_text = get_text("invalid_phone", lang=user_lang)
            await callback.answer(error_text)
            await callback.message.edit_text(error_text)
            await callback.message.answer(get_text("ask_phone", lang=user_lang), reply_markup=get_phone_keyboard())
            await state.set_state(ApplicationStates.waiting_for_phone)
            return
        
        # Phone is confirmed and valid - proceed
        confirm_text = get_text("phone_received", lang=user_lang)
        if confirm_text == "phone_received":
            confirm_text = "✅ Telefon raqami tasdiqlandi!"
        
        await callback.answer(confirm_text)
        await callback.message.edit_text(confirm_text)
        await callback.message.answer(get_text("ask_is_student", lang=user_lang), reply_markup=get_yes_no_keyboard())
        await state.set_state(ApplicationStates.waiting_for_is_student)
        
    elif action == "edit":
        # Edit - go back to phone input (EXACTLY one step back)
        edit_text = get_text("ask_phone", lang=user_lang)
        if edit_text == "ask_phone":
            edit_text = "6️⃣ Telefon raqamingizni kiriting:\n\n📱 Kontakt tugmasini bosing yoki raqamni qo'lda kiriting (+998XXXXXXXXX formatida):"
        
        await callback.answer("✏️ Telefon raqamni o'zgartirish")
        await callback.message.edit_text(edit_text)
        await callback.message.answer(edit_text, reply_markup=get_phone_keyboard())
        await state.set_state(ApplicationStates.waiting_for_phone)


@router.message(ApplicationStates.waiting_for_phone_confirmation)
async def process_phone_confirmation_invalid(message: Message, state: FSMContext):
    """Handle invalid input during phone confirmation (user should use buttons)"""
    # Get user language from state
    data = await state.get_data()
    user_lang = data.get("user_language", "uz")
    
    # If back button, go to phone input
    if message.text == "🔙 Orqaga":
        await message.answer(get_text("ask_phone", lang=user_lang), reply_markup=get_phone_keyboard())
        await state.set_state(ApplicationStates.waiting_for_phone)
        return
    
    # Show confirmation again
    phone = data.get("phone", "")
    confirmation_text = get_text("phone_confirmation_question", lang=user_lang)
    if confirmation_text == "phone_confirmation_question":
        confirmation_text = "Telefon raqamingiz to'g'rimi?"
    
    phone_display = get_text("phone_formatted_display", lang=user_lang)
    if phone_display == "phone_formatted_display":
        phone_display = "📱 Telefon raqami:"
    
    prompt_text = "Iltimos, quyidagi tugmalardan foydalaning:"
    if user_lang != "uz":
        prompt_text = "Please use the buttons below:"
    
    await message.answer(
        f"{prompt_text}\n\n{phone_display}\n`{phone}`\n\n{confirmation_text}",
        parse_mode="Markdown",
        reply_markup=get_phone_confirmation_keyboard()
    )


@router.message(ApplicationStates.waiting_for_is_student)
async def process_is_student(message: Message, state: FSMContext):
    """Process is student question"""
    # Get user language from state
    data = await state.get_data()
    user_lang = data.get("user_language", "uz")
    
    if message.text == "🔙 Orqaga":
        # Go back to phone confirmation (not phone input)
        phone = data.get("phone", "")
        confirmation_text = get_text("phone_confirmation_question", lang=user_lang)
        if confirmation_text == "phone_confirmation_question":
            confirmation_text = "Telefon raqamingiz to'g'rimi?"
        
        phone_display = get_text("phone_formatted_display", lang=user_lang)
        if phone_display == "phone_formatted_display":
            phone_display = "📱 Telefon raqami:"
        
        await message.answer(
            f"{phone_display}\n`{phone}`\n\n{confirmation_text}",
            parse_mode="Markdown",
            reply_markup=get_phone_confirmation_keyboard()
        )
        await state.set_state(ApplicationStates.waiting_for_phone_confirmation)
        return
    
    if message.text.lower() not in ["ha", "yo'q"]:
        await message.answer(get_text("invalid_yes_no", lang=user_lang))
        return
    
    is_student = "Ha" if message.text.lower() == "ha" else "Yo'q"
    # Preserve language when updating data
    await state.update_data(is_student=is_student, user_language=user_lang)
    await message.answer(get_text("ask_education", lang=user_lang), reply_markup=get_education_keyboard())
    await state.set_state(ApplicationStates.waiting_for_education)


@router.callback_query(F.data.startswith("education:"), ApplicationStates.waiting_for_education)
async def process_education(callback: CallbackQuery, state: FSMContext):
    """Process education level"""
    # Get user language from state
    data = await state.get_data()
    user_lang = data.get("user_language", "uz")
    
    education = callback.data.split(":", 1)[1]
    # Preserve language when updating data
    await state.update_data(education=education, user_language=user_lang)
    
    answer_text = get_text("education_selected", lang=user_lang)
    if answer_text == "education_selected":
        answer_text = f"Ma'lumot: {education}"
    await callback.answer(answer_text)
    
    confirmation_text = get_text("education_confirmed", lang=user_lang)
    if confirmation_text == "education_confirmed":
        confirmation_text = f"✅ Ma'lumot: {education}"
    await callback.message.edit_text(confirmation_text)
    await callback.message.answer(get_text("ask_gender", lang=user_lang), reply_markup=get_gender_keyboard())
    await state.set_state(ApplicationStates.waiting_for_gender)


@router.callback_query(F.data.startswith("gender:"), ApplicationStates.waiting_for_gender)
async def process_gender(callback: CallbackQuery, state: FSMContext):
    """Process gender"""
    # Get user language from state
    data = await state.get_data()
    user_lang = data.get("user_language", "uz")
    
    gender = callback.data.split(":", 1)[1]
    # Preserve language when updating data
    await state.update_data(gender=gender, user_language=user_lang)
    
    answer_text = get_text("gender_selected", lang=user_lang)
    if answer_text == "gender_selected":
        answer_text = f"Jins: {gender}"
    await callback.answer(answer_text)
    
    confirmation_text = get_text("gender_confirmed", lang=user_lang)
    if confirmation_text == "gender_confirmed":
        confirmation_text = f"✅ Jins: {gender}"
    await callback.message.edit_text(confirmation_text)
    # Move to language skills
    await callback.message.answer(get_text("ask_russian_level", lang=user_lang), reply_markup=get_language_level_keyboard("russian"))
    await state.set_state(ApplicationStates.waiting_for_russian_level)


# ============================================
# STEP 3: LANGUAGE SKILLS
# ============================================

@router.callback_query(F.data.startswith("russian_level:"), ApplicationStates.waiting_for_russian_level)
async def process_russian_level(callback: CallbackQuery, state: FSMContext):
    """Process Russian language level"""
    # Get user language from state
    data = await state.get_data()
    user_lang = data.get("user_language", "uz")
    
    level = callback.data.split(":", 1)[1]
    # Preserve language when updating data
    await state.update_data(russian_level=level, user_language=user_lang)
    
    answer_text = get_text("russian_level_selected", lang=user_lang)
    if answer_text == "russian_level_selected":
        answer_text = f"Rus tili: {level}"
    await callback.answer(answer_text)
    
    confirmation_text = get_text("russian_level_confirmed", lang=user_lang)
    if confirmation_text == "russian_level_confirmed":
        confirmation_text = f"✅ Rus tili: {level}"
    await callback.message.edit_text(confirmation_text)
    
    # If O'rtacha or Ilg'or, ask for voice message
    if level in ["O'rtacha", "Ilg'or"]:
        await callback.message.answer(get_text("ask_russian_voice", lang=user_lang), reply_markup=get_back_keyboard())
        await state.set_state(ApplicationStates.waiting_for_russian_voice)
    else:
        # Skip to English level
        await callback.message.answer(get_text("ask_english_level", lang=user_lang), reply_markup=get_language_level_keyboard("english"))
        await state.set_state(ApplicationStates.waiting_for_english_level)


@router.message(ApplicationStates.waiting_for_russian_voice, F.voice)
async def process_russian_voice(message: Message, state: FSMContext):
    """Process Russian voice message (≈10 seconds)"""
    # Get user language from state
    data = await state.get_data()
    user_lang = data.get("user_language", "uz")
    
    if message.text == "🔙 Orqaga":
        await message.answer(get_text("ask_russian_level", lang=user_lang), reply_markup=get_language_level_keyboard("russian"))
        await state.set_state(ApplicationStates.waiting_for_russian_level)
        return
    
    duration = message.voice.duration if message.voice else 0
    
    if duration < MIN_AUDIO_DURATION:
        await message.answer(get_text("audio_too_short", lang=user_lang))
        return
    
    file_id = message.voice.file_id
    # Preserve language when updating data
    await state.update_data(russian_voice=file_id, user_language=user_lang)
    
    success_text = get_text("russian_voice_received", lang=user_lang)
    if success_text == "russian_voice_received":
        success_text = "✅ Rus tili audio qabul qilindi!"
    await message.answer(success_text)
    await message.answer(get_text("ask_english_level", lang=user_lang), reply_markup=get_language_level_keyboard("english"))
    await state.set_state(ApplicationStates.waiting_for_english_level)


@router.message(ApplicationStates.waiting_for_russian_voice)
async def process_russian_voice_invalid(message: Message, state: FSMContext):
    """Handle invalid input for Russian voice"""
    # Get user language from state
    data = await state.get_data()
    user_lang = data.get("user_language", "uz")
    
    if message.text == "🔙 Orqaga":
        await message.answer(get_text("ask_russian_level", lang=user_lang), reply_markup=get_language_level_keyboard("russian"))
        await state.set_state(ApplicationStates.waiting_for_russian_level)
        return
    await message.answer(get_text("require_audio", lang=user_lang))


@router.callback_query(F.data.startswith("english_level:"), ApplicationStates.waiting_for_english_level)
async def process_english_level(callback: CallbackQuery, state: FSMContext):
    """Process English language level"""
    # Get user language from state
    data = await state.get_data()
    user_lang = data.get("user_language", "uz")
    
    level = callback.data.split(":", 1)[1]
    # Preserve language when updating data
    await state.update_data(english_level=level, user_language=user_lang)
    
    answer_text = get_text("english_level_selected", lang=user_lang)
    if answer_text == "english_level_selected":
        answer_text = f"Ingliz tili: {level}"
    await callback.answer(answer_text)
    
    confirmation_text = get_text("english_level_confirmed", lang=user_lang)
    if confirmation_text == "english_level_confirmed":
        confirmation_text = f"✅ Ingliz tili: {level}"
    await callback.message.edit_text(confirmation_text)
    
    # If O'rtacha or Ilg'or, ask for voice or video message
    if level in ["O'rtacha", "Ilg'or"]:
        await callback.message.answer(get_text("ask_english_media", lang=user_lang), reply_markup=get_skip_keyboard())
        await state.set_state(ApplicationStates.waiting_for_english_media)
    else:
        # Skip to documents section
        await callback.message.answer(get_text("ask_ielts", lang=user_lang), reply_markup=get_skip_keyboard())
        await state.set_state(ApplicationStates.waiting_for_ielts_certificate)


@router.message(ApplicationStates.waiting_for_english_media, F.voice | F.audio | F.video)
async def process_english_media(message: Message, state: FSMContext):
    """Process English voice/video message"""
    # Get user language from state
    data = await state.get_data()
    user_lang = data.get("user_language", "uz")
    
    if message.voice:
        file_id = message.voice.file_id
        media_type = "voice"
    elif message.audio:
        file_id = message.audio.file_id
        media_type = "audio"
    elif message.video:
        file_id = message.video.file_id
        media_type = "video"
    else:
        await message.answer(get_text("require_media", lang=user_lang))
        return
    
    # Preserve language when updating data
    await state.update_data(english_media=file_id, english_media_type=media_type, user_language=user_lang)
    
    success_text = get_text("english_media_received", lang=user_lang)
    if success_text == "english_media_received":
        success_text = "✅ Ingliz tili media qabul qilindi!"
    await message.answer(success_text)
    await message.answer(get_text("ask_ielts", lang=user_lang), reply_markup=get_skip_keyboard())
    await state.set_state(ApplicationStates.waiting_for_ielts_certificate)


@router.callback_query(F.data == "skip", ApplicationStates.waiting_for_english_media)
async def skip_english_media(callback: CallbackQuery, state: FSMContext):
    """Skip English media"""
    # Get user language from state
    data = await state.get_data()
    user_lang = data.get("user_language", "uz")
    
    # Preserve language when updating data
    await state.update_data(english_media=None, english_media_type=None, user_language=user_lang)
    
    skip_text = get_text("skipped", lang=user_lang)
    if skip_text == "skipped":
        skip_text = "O'tkazib yuborildi"
    await callback.answer(skip_text)
    
    confirmation_text = get_text("skipped_confirmed", lang=user_lang)
    if confirmation_text == "skipped_confirmed":
        confirmation_text = "✅ O'tkazib yuborildi"
    await callback.message.edit_text(confirmation_text)
    await callback.message.answer(get_text("ask_ielts", lang=user_lang), reply_markup=get_skip_keyboard())
    await state.set_state(ApplicationStates.waiting_for_ielts_certificate)


@router.message(ApplicationStates.waiting_for_english_media)
async def process_english_media_invalid(message: Message, state: FSMContext):
    """Handle invalid input for English media"""
    # Get user language from state
    data = await state.get_data()
    user_lang = data.get("user_language", "uz")
    
    await message.answer(get_text("require_media", lang=user_lang))


# ============================================
# STEP 4: DOCUMENTS
# ============================================

@router.message(ApplicationStates.waiting_for_ielts_certificate, F.document)
async def process_ielts_certificate(message: Message, state: FSMContext):
    """Process IELTS certificate (PDF, optional)"""
    # Get user language from state
    data = await state.get_data()
    user_lang = data.get("user_language", "uz")
    
    if message.document.mime_type != "application/pdf":
        await message.answer(get_text("require_pdf", lang=user_lang))
        return
    
    # Preserve language when updating data
    await state.update_data(ielts_certificate=message.document.file_id, user_language=user_lang)
    
    success_text = get_text("ielts_received", lang=user_lang)
    if success_text == "ielts_received":
        success_text = "✅ IELTS sertifikati qabul qilindi!"
    await message.answer(success_text)
    await message.answer(get_text("ask_work_experience", lang=user_lang), reply_markup=get_work_experience_keyboard_reply())
    await state.set_state(ApplicationStates.waiting_for_work_experience)


@router.callback_query(F.data == "skip", ApplicationStates.waiting_for_ielts_certificate)
async def skip_ielts_certificate(callback: CallbackQuery, state: FSMContext):
    """Skip IELTS certificate"""
    # Get user language from state
    data = await state.get_data()
    user_lang = data.get("user_language", "uz")
    
    # Preserve language when updating data
    await state.update_data(ielts_certificate=None, user_language=user_lang)
    
    skip_text = get_text("skipped", lang=user_lang)
    if skip_text == "skipped":
        skip_text = "O'tkazib yuborildi"
    await callback.answer(skip_text)
    
    confirmation_text = get_text("skipped_confirmed", lang=user_lang)
    if confirmation_text == "skipped_confirmed":
        confirmation_text = "✅ O'tkazib yuborildi"
    await callback.message.edit_text(confirmation_text)
    await callback.message.answer(get_text("ask_work_experience", lang=user_lang), reply_markup=get_work_experience_keyboard_reply())
    await state.set_state(ApplicationStates.waiting_for_work_experience)


@router.message(ApplicationStates.waiting_for_ielts_certificate)
async def process_ielts_certificate_invalid(message: Message, state: FSMContext):
    """Handle invalid input for IELTS certificate"""
    # Get user language from state
    data = await state.get_data()
    user_lang = data.get("user_language", "uz")
    
    error_text = get_text("invalid_ielts_input", lang=user_lang)
    if error_text == "invalid_ielts_input":
        error_text = "❌ Iltimos, PDF fayl yuboring yoki 'O'tkazib yuborish' tugmasini bosing:"
    await message.answer(error_text, reply_markup=get_skip_keyboard())


@router.message(ApplicationStates.waiting_for_work_experience)
async def process_work_experience(message: Message, state: FSMContext):
    """Process work experience"""
    # Get user language from state
    data = await state.get_data()
    user_lang = data.get("user_language", "uz")
    
    if message.text == "🔙 Orqaga":
        await message.answer(get_text("ask_ielts", lang=user_lang), reply_markup=get_skip_keyboard())
        await state.set_state(ApplicationStates.waiting_for_ielts_certificate)
        return
    
    # Check if valid experience option
    from bot.config import WORK_EXPERIENCE
    if message.text not in WORK_EXPERIENCE:
        error_text = get_text("invalid_selection", lang=user_lang)
        if error_text == "invalid_selection":
            error_text = "❌ Iltimos, tugmalardan birini tanlang:"
        await message.answer(error_text)
        return
    
    # Preserve language when updating data
    await state.update_data(work_experience=message.text, user_language=user_lang)
    
    confirmation_text = get_text("work_experience_selected", lang=user_lang)
    if confirmation_text == "work_experience_selected":
        confirmation_text = f"✅ Tajriba: {message.text}"
    await message.answer(confirmation_text)
    await message.answer(get_text("ask_last_workplace", lang=user_lang), reply_markup=get_back_keyboard())
    await state.set_state(ApplicationStates.waiting_for_last_workplace)


@router.message(ApplicationStates.waiting_for_last_workplace)
async def process_last_workplace(message: Message, state: FSMContext):
    """Process last workplace and reason for leaving"""
    # Get user language from state
    data = await state.get_data()
    user_lang = data.get("user_language", "uz")
    
    if message.text == "🔙 Orqaga":
        await message.answer(get_text("ask_work_experience", lang=user_lang), reply_markup=get_work_experience_keyboard_reply())
        await state.set_state(ApplicationStates.waiting_for_work_experience)
        return
    
    # Preserve language when updating data
    await state.update_data(last_workplace=message.text, user_language=user_lang)
    await message.answer(get_text("ask_photo", lang=user_lang), reply_markup=get_back_keyboard())
    await state.set_state(ApplicationStates.waiting_for_photo)


@router.message(ApplicationStates.waiting_for_photo, F.photo)
async def process_photo(message: Message, state: FSMContext):
    """Process photo (selfie allowed)"""
    # Get user language from state
    data = await state.get_data()
    user_lang = data.get("user_language", "uz")
    
    photo_id = message.photo[-1].file_id  # Get highest resolution
    # Preserve language when updating data
    await state.update_data(photo=photo_id, user_language=user_lang)
    
    success_text = get_text("photo_received", lang=user_lang)
    if success_text == "photo_received":
        success_text = "✅ Rasm qabul qilindi!"
    await message.answer(success_text)
    await message.answer(get_text("ask_hear_about", lang=user_lang), reply_markup=get_back_keyboard())
    await state.set_state(ApplicationStates.waiting_for_hear_about)


@router.message(ApplicationStates.waiting_for_photo)
async def process_photo_invalid(message: Message, state: FSMContext):
    """Handle invalid input for photo"""
    # Get user language from state
    data = await state.get_data()
    user_lang = data.get("user_language", "uz")
    
    if message.text == "🔙 Orqaga":
        await message.answer(get_text("ask_last_workplace", lang=user_lang), reply_markup=get_back_keyboard())
        await state.set_state(ApplicationStates.waiting_for_last_workplace)
        return
    await message.answer(get_text("require_photo", lang=user_lang))


@router.message(ApplicationStates.waiting_for_hear_about)
async def process_hear_about(message: Message, state: FSMContext):
    """Process 'How did you hear about vacancy?' (text input)"""
    # Get user language from state
    data = await state.get_data()
    user_lang = data.get("user_language", "uz")
    
    if message.text == "🔙 Orqaga":
        await message.answer(get_text("ask_photo", lang=user_lang), reply_markup=get_back_keyboard())
        await state.set_state(ApplicationStates.waiting_for_photo)
        return
    
    # Preserve language when updating data
    await state.update_data(hear_about=message.text, user_language=user_lang)
    
    # Show final review
    data = await state.get_data()
    data['username'] = message.from_user.username or "N/A"
    data['user_id'] = message.from_user.id
    data['submission_date'] = datetime.now().strftime("%d.%m.%Y %H:%M")
    
    summary = format_application_summary(data)
    await message.answer(get_text("review_title", lang=user_lang), parse_mode="Markdown")
    await message.answer(summary)
    await message.answer(get_text("confirm_question", lang=user_lang), reply_markup=get_confirmation_keyboard())
    await state.set_state(ApplicationStates.waiting_for_confirmation)


# ============================================
# STEP 5: FINAL REVIEW & CONFIRMATION
# ============================================

@router.callback_query(F.data.startswith("confirm:"), ApplicationStates.waiting_for_confirmation)
async def process_confirmation(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """Process final confirmation"""
    # Get user language from state
    data = await state.get_data()
    user_lang = data.get("user_language", "uz")
    
    action = callback.data.split(":")[1]
    
    if action == "yes":
        # Submit application to HR group
        data['username'] = callback.from_user.username or "N/A"
        data['user_id'] = callback.from_user.id
        data['submission_date'] = datetime.now().strftime("%d.%m.%Y %H:%M")
        
        summary = format_application_summary(data)
        
        # Validate HR_GROUP_ID before sending
        if HR_GROUP_ID is None:
            logger.error("HR_GROUP_ID is not set or invalid. Cannot send application to HR group.")
            error_answer = get_text("submission_error", lang=user_lang)
            if error_answer == "submission_error":
                error_answer = "❌ Xatolik yuz berdi. Iltimos, qayta urinib ko'ring."
            await callback.answer(error_answer)
            error_message = get_text("error_occurred", lang=user_lang)
            if error_message == "error_occurred":
                error_message = "❌ HR guruhi sozlanmagan. Iltimos, administrator bilan bog'laning."
            await callback.message.answer(error_message)
            menu_text = get_text("return_to_main_menu", lang=user_lang)
            if menu_text == "return_to_main_menu":
                menu_text = "Bosh menyuga qaytish:"
            await callback.message.answer(menu_text, reply_markup=get_main_menu_keyboard())
            saved_lang = user_lang
            await state.clear()
            await state.update_data(user_language=saved_lang)
            return
        
        try:
            # Log the exact chat_id being used
            logger.info(f"Sending application to HR group (chat_id: {HR_GROUP_ID}, type: {type(HR_GROUP_ID).__name__})")
            
            # If photo exists, send photo with short caption, then send full summary as text with keyboard
            # Otherwise, send summary as text message with keyboard
            hr_keyboard = get_hr_decision_keyboard(data['user_id'])
            if data.get('photo'):
                # Send photo with short caption
                short_caption = "📄 New Job Application\n⬇️ Full details below"
                await bot.send_photo(HR_GROUP_ID, data['photo'], caption=short_caption, disable_notification=True)
                # Send full summary as text message with inline keyboard immediately after photo
                await bot.send_message(HR_GROUP_ID, summary, reply_markup=hr_keyboard, disable_notification=True)
            else:
                # Send summary to HR group (silently) with inline keyboard - no photo case
                # IMPORTANT: Use HR_GROUP_ID directly from config (already int), not from state/message
                await bot.send_message(HR_GROUP_ID, summary, reply_markup=hr_keyboard, disable_notification=True)
            
            # Send files if available (these remain as separate messages)
            if data.get('russian_voice'):
                await send_media_to_group(bot, HR_GROUP_ID, data['russian_voice'], "voice", "Rus tili audio (≈10s)")
            
            if data.get('english_media'):
                media_type = data.get('english_media_type', 'audio')
                await send_media_to_group(bot, HR_GROUP_ID, data['english_media'], media_type, "Ingliz tili media")
            
            if data.get('ielts_certificate'):
                await send_media_to_group(bot, HR_GROUP_ID, data['ielts_certificate'], "document", "IELTS sertifikati")
            
            success_answer = get_text("application_submitted", lang=user_lang)
            if success_answer == "application_submitted":
                success_answer = "✅ Arizangiz muvaffaqiyatli yuborildi!"
            await callback.answer(success_answer)
            await callback.message.edit_text(success_answer)
            await callback.message.answer(get_text("thank_you", lang=user_lang), parse_mode="Markdown")
            
            # Send auto reply to applicant
            auto_reply_text = "✅ Arizangiz qabul qilindi!\n\n📅 Arizangiz 3 kun ichida ko'rib chiqiladi.\n🤖 Javob sizga shu bot orqali yuboriladi.\n\nIltimos, kuting."
            await bot.send_message(data['user_id'], auto_reply_text)
            
            menu_text = get_text("return_to_main_menu", lang=user_lang)
            if menu_text == "return_to_main_menu":
                menu_text = "Bosh menyuga qaytish:"
            await callback.message.answer(menu_text, reply_markup=get_main_menu_keyboard())
            
        except Exception as e:
            error_answer = get_text("submission_error", lang=user_lang)
            if error_answer == "submission_error":
                error_answer = "❌ Xatolik yuz berdi. Iltimos, qayta urinib ko'ring."
            await callback.answer(error_answer)
            
            error_message = get_text("error_occurred", lang=user_lang)
            if error_message == "error_occurred":
                error_message = f"❌ Xatolik: {str(e)}"
            await callback.message.answer(error_message)
            
            menu_text = get_text("return_to_main_menu", lang=user_lang)
            if menu_text == "return_to_main_menu":
                menu_text = "Bosh menyuga qaytish:"
            await callback.message.answer(menu_text, reply_markup=get_main_menu_keyboard())
        
        # Preserve language when clearing state
        saved_lang = user_lang
        await state.clear()
        await state.update_data(user_language=saved_lang)
        
    elif action == "back":
        # Go back - restart application (preserve language)
        back_text = get_text("going_back", lang=user_lang)
        if back_text == "going_back":
            back_text = "Orqaga qaytish"
        await callback.answer(back_text)
        
        restart_text = get_text("restart_application", lang=user_lang)
        if restart_text == "restart_application":
            restart_text = "Arizani qayta boshlash uchun '🧳 Bo'sh ish o'rinlari' tugmasini bosing."
        await callback.message.edit_text(restart_text)
        
        menu_text = get_text("main_menu", lang=user_lang)
        if menu_text == "main_menu":
            menu_text = "Bosh menyu:"
        await callback.message.answer(menu_text, reply_markup=get_main_menu_keyboard())
        
        # Preserve language when clearing state
        saved_lang = user_lang
        await state.clear()
        await state.update_data(user_language=saved_lang)


# ============================================
# HR DECISION HANDLERS
# ============================================

@router.callback_query(F.data.startswith("approve_"))
async def handle_approve_application(callback: CallbackQuery, bot: Bot):
    """Handle approve application callback from HR"""
    try:
        # Extract user_id from callback_data (format: approve_{user_id})
        user_id = int(callback.data.split("_", 1)[1])
        
        # Send message to applicant
        message_text = "🎉 Tabriklaymiz!\n\nSiz ishga qabul qilindingiz.\nBatafsil ma'lumot tez orada siz bilan bog'laniladi."
        await bot.send_message(user_id, message_text)
        
        # Answer callback
        await callback.answer("✅ Xabar yuborildi", show_alert=False)
        
        # Edit message to show it was processed
        await callback.message.edit_reply_markup(reply_markup=None)
        
    except (ValueError, IndexError) as e:
        logger.error(f"Error parsing user_id from approve callback: {e}")
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
    except Exception as e:
        logger.error(f"Error sending approve message: {e}")
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)


@router.callback_query(F.data.startswith("interview_"))
async def handle_interview_application(callback: CallbackQuery, bot: Bot):
    """Handle interview invitation callback from HR"""
    try:
        # Extract user_id from callback_data (format: interview_{user_id})
        user_id = int(callback.data.split("_", 1)[1])
        
        # Send message to applicant
        message_text = "📢 Siz suhbat bosqichiga qabul qilindingiz!\n\n📅 Suhbat vaqti va joyi 2 kun ichida sizga yuboriladi.\nIltimos, telefoningiz ochiq bo'lsin."
        await bot.send_message(user_id, message_text)
        
        # Answer callback
        await callback.answer("✅ Xabar yuborildi", show_alert=False)
        
        # Edit message to show it was processed
        await callback.message.edit_reply_markup(reply_markup=None)
        
    except (ValueError, IndexError) as e:
        logger.error(f"Error parsing user_id from interview callback: {e}")
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
    except Exception as e:
        logger.error(f"Error sending interview message: {e}")
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)


@router.callback_query(F.data.startswith("reject_"))
async def handle_reject_application(callback: CallbackQuery, bot: Bot):
    """Handle reject application callback from HR"""
    try:
        # Extract user_id from callback_data (format: reject_{user_id})
        user_id = int(callback.data.split("_", 1)[1])
        
        # Send message to applicant
        message_text = "Rahmat.\n\nAfsuski, hozircha sizning arizangiz tasdiqlanmadi.\nKeyingi imkoniyatlarda yana urinib ko'rishingiz mumkin."
        await bot.send_message(user_id, message_text)
        
        # Answer callback
        await callback.answer("✅ Xabar yuborildi", show_alert=False)
        
        # Edit message to show it was processed
        await callback.message.edit_reply_markup(reply_markup=None)
        
    except (ValueError, IndexError) as e:
        logger.error(f"Error parsing user_id from reject callback: {e}")
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
    except Exception as e:
        logger.error(f"Error sending reject message: {e}")
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)