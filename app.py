from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from datetime import datetime, timedelta
import pytz

app = Flask(__name__)

line_bot_api = LineBotApi("2DvhpZfivG8RN2/cwP+u1VF86IVc/lcj9Q2cSAG17beIeJsSUqwdUhxtUk9Coxi0/iq1S4Sf9xtPgh/WamPCqq77vUh4Dzu5nt8VkwE5ZP4ctOn02jQO7tq7yDc8GJ7k+Y5WuWpaKXc6Ud55LCEN9QdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("ba1527c64b8a6b7a22a84675e8879df2")

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text.lower()
    
    if (
        "ชุด3เข้าเวร" in user_text
        or "ชุด3 เข้าเวร" in user_text
        or "เวรคืนนี้" in user_text
    ):
        tz = pytz.timezone('Asia/Bangkok')
        today = datetime.now(tz)
        tomorrow = today + timedelta(days=1)

        thai_months = [
            "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
            "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"
        ]

        def thai_date(date_obj):
            return f"{date_obj.day} {thai_months[date_obj.month - 1]} {date_obj.year + 543}"

        msg = (
            f"สภ.ปากคลองรังสิต\n"
            f"-------------------\n\n"
            f"เรียนผู้บังคับบัญชา\n\n"
            f"วันที่ {thai_date(today)}\n"
            f"ร.ต.อ.เกียรติศักดิ์ คำกุล รอง สว.สส.ฯ\n"
            f"ส.ต.อ.ธีระ โฉมไธสง\n"
            f"ส.ต.ท.ปภาวินทร์ ทิพย์ธารทอง\n\n"
            f"ปฏิบัติหน้าที่ เวรสืบสวนประจำวันนี้\n"
            f"ตั้งแต่วันที่ {thai_date(today)} เวลา 08.00 น.\n"
            f"ถึง 08.00 น. ของวันที่ {thai_date(tomorrow)}\n\n"
            f"-------------------\n"
            f"จึงเรียนมาเพื่อโปรดทราบ"
        )

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=msg)
        )