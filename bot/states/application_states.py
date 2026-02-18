from aiogram.fsm.state import State, StatesGroup


class ApplicationStates(StatesGroup):
    """FSM states for job application process - EXACT ORDER AS SPECIFIED"""
    
    # Step 1: Vacancy Selection
    waiting_for_branch = State()  # Reply buttons
    waiting_for_department = State()  # Reply buttons
    waiting_for_position = State()  # INLINE buttons
    
    # Step 2: Personal Information (one by one, ALL required)
    waiting_for_passport_name = State()
    waiting_for_passport_surname = State()
    waiting_for_father_name = State()
    waiting_for_date_of_birth = State()
    waiting_for_address = State()
    waiting_for_phone = State()
    waiting_for_phone_confirmation = State()
    waiting_for_is_student = State()
    waiting_for_education = State()
    waiting_for_gender = State()
    
    # Step 3: Language Skills
    waiting_for_russian_level = State()
    waiting_for_russian_voice = State()  # Only if O'rtacha or Ilg'or
    waiting_for_english_level = State()
    waiting_for_english_media = State()  # Only if O'rtacha or Ilg'or
    
    # Step 4: Documents
    waiting_for_ielts_certificate = State()  # Optional
    waiting_for_work_experience = State()
    waiting_for_last_workplace = State()
    waiting_for_photo = State()
    waiting_for_hear_about = State()  # Text input
    
    # Step 5: Final Review & Confirmation
    waiting_for_confirmation = State()
