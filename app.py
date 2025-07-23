@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text.lower()

    if (
        "ชุด3เข้าเวร" in user_text
        or "ชุด3 เข้าเวร" in user_text
        or "เวรคืนนี้" in user_text
    ):
        tz = pytz.timezone('Asia/Bangkok')  # ✅ ตั้ง timezone เป็นไทย
        today = datetime.now(tz)
        tomorrow = today + timedelta(days=1)

        thai_months = [
            "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
            "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"
        ]

        def thai_date(date_obj):
            return f"{date_obj.day} {thai_months[date_obj.month - 1]} {date_obj.year + 543}"

        msg = f"""สภ.ปากคลองรังสิต  
-------------------

เรียนผู้บังคับบัญชา

วันที่ {thai_date(today)}  
ร.ต.อ.เกียรติศักดิ์ คำกุล รอง สว.สส.ฯ  
ส.ต.อ.ธีระ โฉมไธสง  
ส.ต.ท.ปภาวินทร์ ทิพย์ธารทอง

ปฏิบัติหน้าที่ เวรสืบสวนประจำวันนี้  
ตั้งแต่วันที่ {thai_date(today)} เวลา 08.00 น.  
ถึง 08.00 น. ของวันที่ {thai_date(tomorrow)}  

-------------------  
จึงเรียนมาเพื่อโปรดทราบ"""

