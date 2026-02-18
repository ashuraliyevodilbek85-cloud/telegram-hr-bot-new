"""Text messages for the bot with multi-language support"""
from bot.config import COMPANY_NAME, BOT_NAME

# Uzbek texts
TEXTS_UZ = {
    "start_welcome": f"""👋 Salom!

Xush kelibsiz, **{BOT_NAME}** botiga!

🏢 **{COMPANY_NAME}** ga ish topish uchun ariza berish uchun quyidagi tugmalardan foydalaning.

Kompaniya haqida qisqacha ma'lumot:
{COMPANY_NAME} - bu professional ta'lim markazi bo'lib, eng yaxshi ta'lim xizmatlarini taklif etamiz.

Boshlash uchun quyidagi tugmani bosing:""",
    
    "main_menu": "Bosh menyu",
    
    "about_company": f"""🏢 **{COMPANY_NAME} HAQIDA**

{COMPANY_NAME} - bu professional ta'lim markazi bo'lib, eng yaxshi ta'lim xizmatlarini taklif etamiz.

Bizning filiallarimiz:
• Clara
• Severniy
• Business Center
• Yangi Bozor

Bizning bo'limlarimiz:
🧠 Akademik bo'lim
💼 Sotuv bo'limi
📱 SMM bo'limi
⚙️ Operational Team

Bizga qo'shiling va professional jamoaning bir qismi bo'ling!""",
    
    "contacts": """☎️ **KONTAKTLAR**

Biz bilan bog'lanish uchun:
• Telegram: @proper_english_school
• Telefon: +998 XX XXX XX XX
• Email: info@properenglish.uz

Ish vaqti: Dushanba - Yakshanba, 9:00 - 18:00""",
    
    "feedback": """💬 **FIKR-MULOHAZALAR**

Sizning fikr va mulohazalaringiz biz uchun muhim!

Iltimos, fikr-mulohazalaringizni yozib qoldiring:""",
    
    "language_change": """🌐 **TILNI O'ZGARTIRISH**

Quyidagi tillardan birini tanlang:""",
    "language_changed": "✅ Til muvaffaqiyatli o'zgartirildi!",
    
    "vacancy_start": """🧳 **BO'SH ISH O'RINLARI**

Ish arizasini to'ldirish uchun quyidagi bosqichlarni bajarishingiz kerak:

1️⃣ Filial tanlash
2️⃣ Bo'lim tanlash
3️⃣ Lavozim tanlash (inline tugmalar)
4️⃣ Shaxsiy ma'lumotlarni kiritish
5️⃣ Til bilimini ko'rsatish
6️⃣ Ish tajribasini ko'rsatish
7️⃣ Qo'shimcha ma'lumotlar
8️⃣ Tasdiqlash

⚠️ Eslatma: Barcha ma'lumotlarni to'liq va to'g'ri kiriting.

Filialni tanlang:""",
    
    "select_branch": "Filialni tanlang:",
    "select_department": "Bo'limni tanlang:",
    "select_position": "Lavozimni tanlang (inline tugmalar):",
    
    "personal_info": "📝 Endi shaxsiy ma'lumotlarni kiriting (barcha maydonlar majburiy):",
    "ask_passport_name": "1️⃣ Pasportdagi ismingizni kiriting:",
    "ask_passport_surname": "2️⃣ Pasportdagi familiyangizni kiriting:",
    "ask_father_name": "3️⃣ Otangizning ismini kiriting:",
    "ask_date_of_birth": "4️⃣ Tug'ilgan sanangizni kiriting (DD.MM.YYYY formatida, masalan: 01.01.2000):",
    "ask_address": "5️⃣ To'liq manzilingizni kiriting:",
    "ask_phone": """6️⃣ Telefon raqamingizni kiriting:

📱 Kontakt tugmasini bosing yoki raqamni qo'lda kiriting (+998XXXXXXXXX formatida):""",
    "phone_received": "📱 Telefon raqami qabul qilindi!",
    "phone_confirmation_question": "Telefon raqamingiz to'g'rimi?",
    "phone_formatted_display": "📱 Telefon raqami:",
    "ask_is_student": "7️⃣ Talabamisiz?",
    "ask_education": "8️⃣ Ma'lumotingizni tanlang:",
    "ask_gender": "9️⃣ Jinsingizni tanlang:",
    
    "ask_russian_level": "🔟 Rus tilidagi darajangizni tanlang:",
    "ask_russian_voice": """Rus tilida o'zingizni tanishtiring (AUDIO xabar, kamida ≈10 soniya):

Quyidagi mavzular haqida gapiring:
• O'zingiz haqingizda
• Ta'lim
• Ish tajribasi""",
    
    "ask_english_level": "1️⃣1️⃣ Ingliz tilidagi darajangizni tanlang:",
    "ask_english_media": """Ingliz tilida o'zingizni tanishtiring (AUDIO yoki VIDEO xabar):

Quyidagi ma'lumotlarni kiriting:
• Yoshingiz
• Shift (ish vaqti)
• Ta'lim (BA/MA + IELTS bo'lsa)
• Tajriba
• Murojaat qilayotgan lavozim""",
    
    "ask_ielts": "1️⃣2️⃣ IELTS sertifikatingizni yuklang (PDF, ixtiyoriy):",
    "ask_work_experience": "1️⃣3️⃣ Ish tajribangizni tanlang:",
    "ask_last_workplace": "Oxirgi ish joyingiz va ketish sababingizni yozing:",
    "ask_photo": "1️⃣4️⃣ Rasm yuklang (selfie ruxsat etiladi):",
    "ask_hear_about": "1️⃣5️⃣ Biz haqimizda qayerdan eshitdingiz? (Matn sifatida yozing):",
    "ask_cv": "1️⃣6️⃣ CV yuklang (PDF):",
    
    "review_title": "📋 **ARIZA TO'LIQ MA'LUMOTLARI:**",
    "confirm_question": "⚠️ Barcha ma'lumotlar to'g'rimi? Tasdiqlang:",
    
    "thank_you": """✅ **Arizangiz muvaffaqiyatli yuborildi!**

Sizning arizangiz HR bo'limiga yuborildi. Tez orada siz bilan bog'lanamiz.

Rahmat!""",
    
    "invalid_date": "❌ Noto'g'ri format! Iltimos, DD.MM.YYYY formatida kiriting (masalan: 01.01.2000):",
    "invalid_phone": """❌ Noto'g'ri telefon raqami!

Iltimos, quyidagi formatlardan birini kiriting:
• +998901234567
• 998901234567
• 901234567

Yoki 📱 Kontakt tugmasini bosing.""",
    "invalid_yes_no": "❌ Iltimos, 'Ha' yoki 'Yo'q' tugmalaridan birini tanlang:",
    "audio_too_short": "❌ Audio xabar juda qisqa! Iltimos, kamida ≈10 soniyalik audio yuboring:",
    "require_audio": "❌ Iltimos, AUDIO xabar yuboring (kamida ≈10 soniya):",
    "require_media": "❌ Iltimos, AUDIO yoki VIDEO yuboring:",
    "require_pdf": "❌ Iltimos, PDF fayl yuboring:",
    "require_photo": "❌ Iltimos, rasm yuboring:",
    "require_cv": "❌ Iltimos, PDF formatida CV yuboring (majburiy):",
}

# Russian texts (for future implementation)
TEXTS_RU = {
    # Can be added later
}

# English texts (basic fallback - uses Uzbek if missing)
TEXTS_EN = {
    "language_change": "🌐 **CHANGE LANGUAGE**\n\nPlease select a language:",
    "language_changed": "✅ Language changed successfully!",
    "main_menu": "Main Menu",
    "about_company": f"""🏢 **ABOUT {COMPANY_NAME}**

{COMPANY_NAME} is a professional educational center offering the best educational services.

Our branches:
• Clara
• Severniy
• Business Center
• Yangi Bozor

Our departments:
🧠 Academic Department
💼 Sales Department
📱 SMM Department
⚙️ Operational Team

Join us and become part of a professional team!""",
    "contacts": """☎️ **CONTACTS**

To contact us:
• Telegram: @proper_english_school
• Phone: +998 XX XXX XX XX
• Email: info@properenglish.uz

Working hours: Monday - Sunday, 9:00 - 18:00""",
    "feedback": """💬 **FEEDBACK**

Your opinions and suggestions are important to us!

Please leave your feedback:""",
    # Other texts will fallback to Uzbek or key name
}

def get_text(key: str, lang: str = "uz") -> str:
    """Get text by key and language with fallback"""
    if lang == "uz":
        texts = TEXTS_UZ
    elif lang == "ru":
        texts = TEXTS_RU
    elif lang == "en":
        texts = TEXTS_EN
    else:
        texts = TEXTS_UZ  # Default fallback
    
    # If text not found in current language, try Uzbek, then return key
    if key not in texts:
        if lang != "uz" and key in TEXTS_UZ:
            return TEXTS_UZ[key]
        return key
    
    return texts.get(key, key)
