import telebot
from telebot import types
import time
import os

# این مقادیر رو بعداً توی سایت Railway وارد می‌کنیم
API_TOKEN = os.getenv('BOT_TOKEN')
YOUR_PERSONAL_ID = int(os.getenv('ADMIN_ID', '0'))

bot = telebot.TeleBot(API_TOKEN)
user_last_msg_time = {}

def is_spamming(user_id):
    current_time = time.time()
    last_time = user_last_msg_time.get(user_id, 0)
    if current_time - last_time < 5:
        return True
    user_last_msg_time[user_id] = current_time
    return False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    markup = types.InlineKeyboardMarkup()
    btn_check = types.InlineKeyboardButton("🔍 استعلام حجم", callback_data="check_volume")
    markup.add(btn_check)
    bot.send_message(message.chat.id, f"سلام {user_name} خوش اومدی!", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "check_volume")
def ask_for_code(call):
    if is_spamming(call.from_user.id):
        bot.answer_callback_query(call.id, "⚠️ لطفاً اسپم نکنید!")
        return
    msg = bot.send_message(call.message.chat.id, "لطفاً کد اشتراک خود را ارسال کنید (مثال: vip1234)")
    bot.register_next_step_handler(msg, process_subscription_code)

def process_subscription_code(message):
    sub_code = message.text
    if sub_code.lower().startswith("vip") and len(sub_code) > 3:
        code_part = sub_code[3:].strip()
        if code_part.isdigit() and len(code_part) <= 4:
            user_info = f"ID:{message.chat.id}\n📥 درخواست جدید\n👤 نام: {message.from_user.first_name}\n🔢 کد: {sub_code}"
            user_reply = "✅ درخواست شما دریافت شد تا دقایقی دیگر استعلام از پنل برا شما ارسال خواهد شد.\n\n✨ نکته: بدلیل اختلال احتمالی در پنل و دامنه ir صبور باشید و از اسپم خودداری کنید."
            bot.send_message(YOUR_PERSONAL_ID, user_info, parse_mode='Markdown')
            bot.send_message(message.chat.id, user_reply)
        else:
            bot.send_message(message.chat.id, "❌ خطا: بخش عددی نباید بیشتر از ۴ رقم باشد.")
    else:
        bot.send_message(message.chat.id, "❌ خطا: کد باید با vip شروع شود.")

@bot.message_handler(func=lambda m: m.reply_to_message is not None and m.from_user.id == YOUR_PERSONAL_ID)
def reply_to_user(message):
    try:
        original_msg = message.reply_to_message.text
        user_id = original_msg.split('\n')[0].replace('ID:', '').strip()
        bot.send_message(user_id, message.text)
        bot.reply_to(message, "✅ ارسال شد.")
    except:
        bot.reply_to(message, "❌ خطا در یافتن آیدی کاربر.")

if name == "main":
    print("Shadow is starting...")
    bot.infinity_polling()