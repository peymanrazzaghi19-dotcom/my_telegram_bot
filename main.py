import telebot
import os

API_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID', '0'))
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("🔍 استعلام حجم", callback_data="check"))
    bot.send_message(message.chat.id, f"سلام {message.from_user.first_name} خوش اومدی!", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "check")
def ask(call):
    msg = bot.send_message(call.message.chat.id, "لطفاً کد اشتراک (مثال: vip1234) را بفرستید:")
    bot.register_next_step_handler(msg, process)

def process(message):
    code = message.text
    if code.lower().startswith("vip"):
        bot.send_message(ADMIN_ID, f"ID:{message.chat.id}\n👤: {message.from_user.first_name}\n🔢: `{code}`", parse_mode='Markdown')
        bot.send_message(message.chat.id, "✅ درخواست شما ارسال شد.")
    else:
        bot.send_message(message.chat.id, "❌ کد باید با vip شروع شود.")

@bot.message_handler(func=lambda m: m.reply_to_message and m.from_user.id == ADMIN_ID)
def reply(message):
    try:
        uid = message.reply_to_message.text.split('\n')[0].replace('ID:', '').strip()
        bot.send_message(uid, message.text)
        bot.reply_to(message, "✅ ارسال شد.")
    except:
        bot.reply_to(message, "❌ خطا در یافتن آیدی.")

if __name__ == "__main__":
    print("Shadow is starting...")
    bot.infinity_polling()
