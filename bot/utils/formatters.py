def format_application_summary(data: dict) -> str:
    """Format application data into a readable summary for HR group"""
    # Map fields to new format
    first_name = data.get("passport_name", "N/A")
    last_name = data.get("passport_surname", "N/A")
    birth_date = data.get("date_of_birth", "N/A")
    experience = data.get("work_experience", "N/A")
    experience_note = data.get("last_workplace", "N/A")
    ielts_status = "Bor" if data.get("ielts_certificate") else "Yo'q"

    summary = f"""📌 YANGI ISH ARIZASI

🏢 Filial: {data.get('branch', 'N/A')}
📍 Shahar: {data.get('city', 'N/A')}
💼 Lavozim: {data.get('position', 'N/A')}
📅 Sana: {data.get('submission_date', 'N/A')}

👤 SHAXSIY MA'LUMOT:
• Ism: {first_name} {last_name}
• Tug'ilgan sana: {birth_date}
• Manzil: {data.get('address', 'N/A')}
• Telefon: {data.get('phone', 'N/A')}
• Ma'lumoti: {data.get('education', 'N/A')}

🗣 TIL DARAJASI:
• Rus tili: {data.get('russian_level', 'N/A')}
• Ingliz tili: {data.get('english_level', 'N/A')}
• IELTS: {ielts_status}

💼 TAJRIBA:
• Tajriba: {experience}
• Izoh: {experience_note}

👤 Telegram: @{data.get('username', 'N/A')}
🆔 ID: {data.get('user_id', 'N/A')}"""
    return summary
