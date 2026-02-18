# Work at Proper - HR Recruitment Bot

Professional Telegram HR recruitment bot for **Proper English School** using Python and aiogram 3.x.

## 🎯 Overview

This bot handles the complete job application process for Proper English School. It collects applicant information step-by-step through an FSM-based flow and sends all applications directly to a private HR Telegram group.

## ✨ Features

- ✅ **FSM-based architecture** - Clean, scalable state management
- ✅ **Step-by-step data collection** - No skipped steps, all fields validated
- ✅ **Multi-language support** - Uzbek and Russian (Uzbek default)
- ✅ **File uploads** - PDF (CV, IELTS), photos, voice, video messages
- ✅ **Smart navigation** - Back button support throughout the flow
- ✅ **HR group integration** - Applications sent silently to private HR group
- ✅ **Reply keyboards** - All menus at bottom (except inline job selection buttons)
- ✅ **Inline buttons** - Job positions selection only

## 🏢 Company Information

- **Company Name**: Proper English School
- **Bot Name**: Work at Proper
- **Work Region**: Andijon only
- **Languages**: 🇺🇿 O'zbek, 🇷🇺 Русский

## 📋 Application Flow

1. **Start** - Welcome message with company intro
2. **Main Menu** - Bottom keyboard with options
3. **Vacancy Selection**:
   - Branch selection (reply buttons)
   - Department selection (reply buttons)
   - Position selection (inline buttons)
4. **Personal Information**:
   - Passport name, surname, father's name
   - Date of birth (DD.MM.YYYY)
   - Full address
   - Phone number (+998XXXXXXXXX)
   - Student status (Yes/No)
   - Education level
   - Gender
5. **Language Skills**:
   - Russian level (if O'rtacha/Ilg'or → voice message required)
   - English level (if O'rtacha/Ilg'or → voice/video required)
6. **Documents**:
   - IELTS certificate (PDF, optional)
   - Work experience
   - Last workplace & reason
   - Photo (selfie allowed)
   - How did you hear about us (text)
   - CV (PDF, required)
7. **Review & Confirmation** - Full summary review
8. **Submission** - Sent to HR group

## 🚀 Installation

### Prerequisites

- Python 3.8+
- pip

### Setup Steps

1. **Clone the repository**:
```bash
git clone <repository-url>
cd my_project
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Create `.env` file**:
```bash
cp .env.example .env
```

4. **Configure `.env` file**:
```env
BOT_TOKEN=your_bot_token_from_botfather
HR_GROUP_ID=your_telegram_group_id
```

**How to get values:**
- **BOT_TOKEN**: Create a bot using [@BotFather](https://t.me/BotFather) on Telegram
- **HR_GROUP_ID**: 
  1. Create a Telegram group for HR
  2. Add [@userinfobot](https://t.me/userinfobot) to the group
  3. Send any message in the group
  4. Check the group ID (usually negative, e.g., -1001234567890)
  5. Make sure your bot is added to the group as admin

## 🏃 Running

```bash
python bot/main.py
```

Or using run.py:
```bash
python run.py
```

## 📁 Project Structure

```
bot/
├── __init__.py
├── config.py              # Configuration (company, branches, departments, etc.)
├── main.py                # Bot entry point and dispatcher setup
├── handlers/
│   ├── __init__.py
│   ├── main_handlers.py   # Start command, main menu handlers
│   └── application_handlers.py  # Full application flow handlers
├── keyboards/
│   ├── __init__.py
│   ├── reply_keyboards.py # Bottom menu keyboards (reply buttons)
│   └── inline_keyboards.py # Inline keyboards (job positions)
├── states/
│   ├── __init__.py
│   └── application_states.py  # FSM states for application flow
└── utils/
    ├── __init__.py
    ├── texts.py           # Multi-language text messages
    ├── validators.py      # Phone, date validation
    ├── formatters.py      # Application summary formatting
    └── file_handlers.py   # File upload/download handlers
```

## 🔧 Configuration

Edit `bot/config.py` to customize:

- **Company name**: `COMPANY_NAME`
- **Bot name**: `BOT_NAME`
- **Branches**: `BRANCHES` dictionary
- **Departments**: `DEPARTMENTS` dictionary
- **Positions**: `POSITIONS` dictionary (organized by department)
- **Languages**: `SUPPORTED_LANGUAGES`
- **Minimum audio duration**: `MIN_AUDIO_DURATION`

## 📝 Usage

1. User sends `/start` command
2. Bot shows welcome message with "Start" button
3. User clicks "Start" → Main menu appears
4. User selects "🧳 Bo'sh ish o'rinlari"
5. Follow step-by-step application process
6. Review and confirm application
7. Application automatically sent to HR Telegram group

## 🔒 HR Group Rules

- Applications sent **silently** (disable_notification=True)
- Only HR admins can access the group
- Applicants never see group or HR actions
- All data formatted neatly with emojis
- Files attached properly (photos, PDFs, voice, video)

## 🛠️ Technical Details

- **Framework**: aiogram 3.x
- **State Management**: FSMContext with MemoryStorage
- **Validation**: Phone numbers, dates, file types
- **Error Handling**: Comprehensive error messages
- **Code Quality**: Clean, readable, production-ready

## 📞 Support

For issues or questions, please contact the development team.

## 📄 License

Proprietary - Proper English School
