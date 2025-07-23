from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from datetime import datetime, timedelta

app = Flask(__name__)

# 🔒 Access Token & Channel Secret
line_bot_api = LineBotApi('2DvhpZfivG8RN2/cwP+u1VF86IVc/lcj9Q2cSAG17beIeJsSUqwdUhxtUk9Coxi0/iq1S4Sf9xtPgh/WamPCqq77vUh4Dzu5nt8VkwE5ZP4ctOn02jQO7tq7yDc8GJ7k+Y5WuWpaKXc6Ud55LCEN9QdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ba1527c64b8a6b7a22a84675e8879df2')

# 📌 Webhook Endpoint
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 💬 ตอบเมื่อพิมพ์ "ชุด3เข้าเวร"
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text.lower()

    if "ชุด3เข้าเวร" in user_text:
        today = datetime.now()
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

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=msg)
        )
