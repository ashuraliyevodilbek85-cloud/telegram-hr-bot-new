"""Main handlers for start command and menu"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.keyboards.reply_keyboards import get_main_menu_keyboard, get_start_keyboard, get_main_menu_back_keyboard
from bot.keyboards.inline_keyboards import get_language_selection_keyboard
from bot.utils.texts import get_text
from bot.config import COMPANY_NAME, BOT_NAME, DEFAULT_LANGUAGE

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """Handle /start command - Welcome message and Start button"""
    # Preserve user language before clearing
    data = await state.get_data()
    saved_lang = data.get("user_language", DEFAULT_LANGUAGE)
    
    await state.clear()  # Clear any previous state
    
    # Restore user language
    await state.update_data(user_language=saved_lang)
    
    welcome_text = get_text("start_welcome", lang=saved_lang)
    
    await message.answer(
        welcome_text,
        parse_mode="Markdown",
        reply_markup=get_start_keyboard()
    )


@router.message(F.text == "▶️ Start")
async def process_start(message: Message, state: FSMContext):
    """Process Start button - Show main menu"""
    # Preserve user language before clearing
    data = await state.get_data()
    saved_lang = data.get("user_language", DEFAULT_LANGUAGE)
    
    await state.clear()
    
    # Restore user language
    await state.update_data(user_language=saved_lang)
    
    await message.answer(
        get_text("main_menu", lang=saved_lang),
        reply_markup=get_main_menu_keyboard()
    )


@router.message(F.text == "🧳 Bo'sh ish o'rinlari")
async def show_vacancies(message: Message, state: FSMContext):
    """Show vacancies and start application process"""
    # Preserve user language before clearing
    data = await state.get_data()
    saved_lang = data.get("user_language", DEFAULT_LANGUAGE)
    
    await state.clear()
    
    # Restore user language and store previous menu for back button
    await state.update_data(user_language=saved_lang, previous_menu="main_menu")
    
    text = get_text("vacancy_start", lang=saved_lang)
    await message.answer(text, parse_mode="Markdown")
    
    # Ask for branch selection (reply buttons)
    from bot.keyboards.reply_keyboards import get_branch_keyboard
    from bot.states.application_states import ApplicationStates
    
    await message.answer(
        get_text("select_branch", lang=saved_lang),
        reply_markup=get_branch_keyboard()
    )
    await state.set_state(ApplicationStates.waiting_for_branch)


@router.message(F.text == "🏢 Kompaniya haqida")
async def show_about(message: Message, state: FSMContext):
    """Show company information"""
    # Get user language
    data = await state.get_data()
    user_lang = data.get("user_language", DEFAULT_LANGUAGE)
    
    # Store that we're in a menu action (for back button)
    await state.update_data(previous_menu="main_menu")
    
    text = get_text("about_company", lang=user_lang)
    await message.answer(text, parse_mode="Markdown", reply_markup=get_main_menu_back_keyboard())


@router.message(F.text == "☎️ Kontaktlar")
async def show_contacts(message: Message, state: FSMContext):
    """Show contact information"""
    # Get user language
    data = await state.get_data()
    user_lang = data.get("user_language", DEFAULT_LANGUAGE)
    
    # Store that we're in a menu action (for back button)
    await state.update_data(previous_menu="main_menu")
    
    text = get_text("contacts", lang=user_lang)
    await message.answer(text, parse_mode="Markdown", reply_markup=get_main_menu_back_keyboard())


@router.message(F.text == "💬 Fikr-mulohazalar")
async def show_feedback(message: Message, state: FSMContext):
    """Show feedback form"""
    # Get user language
    data = await state.get_data()
    user_lang = data.get("user_language", DEFAULT_LANGUAGE)
    
    # Store that we're in a menu action (for back button)
    await state.update_data(previous_menu="main_menu")
    
    text = get_text("feedback", lang=user_lang)
    await message.answer(text, parse_mode="Markdown", reply_markup=get_main_menu_back_keyboard())


@router.message(F.text == "🌐 Tilni o'zgartirish")
async def change_language(message: Message, state: FSMContext):
    """Change language - show language selection keyboard"""
    # Get user language
    data = await state.get_data()
    user_lang = data.get("user_language", DEFAULT_LANGUAGE)
    
    # Store that we're in a menu action (for back button)
    await state.update_data(previous_menu="main_menu")
    
    text = get_text("language_change", lang=user_lang)
    await message.answer(
        text, 
        parse_mode="Markdown", 
        reply_markup=get_language_selection_keyboard()
    )


@router.callback_query(F.data.startswith("lang:"))
async def process_language_selection(callback: CallbackQuery, state: FSMContext):
    """Process language selection"""
    lang_code = callback.data.split(":", 1)[1]
    
    # Validate language code
    from bot.config import SUPPORTED_LANGUAGES
    if lang_code not in SUPPORTED_LANGUAGES:
        await callback.answer("❌ Invalid language selection")
        return
    
    # Store language preference in FSM state
    await state.update_data(user_language=lang_code)
    
    # Get language label
    lang_label = SUPPORTED_LANGUAGES[lang_code]
    
    # Answer callback
    await callback.answer(f"✅ Language changed to {lang_label}")
    
    # Get success message in selected language
    success_text = get_text("language_changed", lang=lang_code)
    if success_text == "language_changed":  # Fallback if not translated
        success_text = f"✅ {lang_label} tanlandi!"
    
    await callback.message.edit_text(success_text)
    
    # Show main menu with back button
    await callback.message.answer(
        get_text("main_menu", lang=lang_code),
        reply_markup=get_main_menu_back_keyboard()
    )


@router.message(F.text == "⬅️ Orqaga")
async def handle_main_menu_back_button(message: Message, state: FSMContext):
    """Handle back button for main menu actions - go back to main menu"""
    data = await state.get_data()
    user_lang = data.get("user_language", DEFAULT_LANGUAGE)
    previous_menu = data.get("previous_menu")
    current_state = await state.get_state()
    
    # If we're in application flow (FSM state is set), don't handle here
    # Application handlers use "🔙 Orqaga" and handle their own back logic
    if current_state is not None:
        return
    
    # If we're in a menu action (Company, Contacts, Feedback, Language), go back to main menu
    if previous_menu == "main_menu":
        await state.update_data(previous_menu=None)
        await message.answer(
            get_text("main_menu", lang=user_lang),
            reply_markup=get_main_menu_keyboard()
        )
        return
    
    # Default: go to main menu (fallback)
    await state.update_data(previous_menu=None)
    await message.answer(
        get_text("main_menu", lang=user_lang),
        reply_markup=get_main_menu_keyboard()
    )
