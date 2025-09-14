# pip install pyTelegramBotAPI requests

import telebot
import requests
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

BOT_TOKEN = "8390430508:AAHv8TY9qbW93uPz1YtJXzPCbrEIgpYStFM"
bot = telebot.TeleBot(BOT_TOKEN)

def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(KeyboardButton("📱 Number Search"), KeyboardButton("🆔 Aadhaar Search"))
    markup.row(KeyboardButton("ℹ️ Help"))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Welcome! Choose an option:",
        reply_markup=main_menu()
    )

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(
        message.chat.id,
        "ℹ️ *Help Menu*\n\n"
        "🔹 Number Search → Send a 10-digit mobile number.\n"
        "🔹 Aadhaar Search → Send a 12-digit Aadhaar/ID number.\n\n"
        "Use keyboard buttons or commands:\n"
        "/num <10-digit-number>\n"
        "/adhar <12-digit-number>\n\n"
        "✅ Free & Unlimited for all!",
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda message: True)
def menu_handler(message):
    text = message.text
    if text == "📱 Number Search":
        bot.send_message(message.chat.id, "📱 Send me a 10-digit mobile number without country code:\nExample: 7037714035")
        bot.register_next_step_handler(message, number_lookup)
    elif text == "🆔 Aadhaar Search":
        bot.send_message(message.chat.id, "🆔 Send me a 12-digit Aadhaar/ID number:\nExample: 919052111598")
        bot.register_next_step_handler(message, aadhaar_lookup)
    elif text == "ℹ️ Help":
        help_command(message)
    elif text and text.startswith("/num"):
        args = text.split(maxsplit=1)
        if len(args) == 2:
            message.text = args[1]
            number_lookup(message)
        else:
            bot.send_message(message.chat.id, "Usage: /num <10-digit-number>\nExample: /num 7037714035")
    elif text and text.startswith("/adhar"):
        args = text.split(maxsplit=1)
        if len(args) == 2:
            message.text = args[1]
            aadhaar_lookup(message)
        else:
            bot.send_message(message.chat.id, "Usage: /adhar <12-digit-number>\nExample: /adhar 919052111598")

def format_result(d, index):
    return (
        f"🔎 Result {index}:\n"
        f"📱 Mobile: {d.get('mobile', 'N/A')}\n"
        f"👤 Name: {d.get('name', 'N/A')}\n"
        f"👨👩👦 Father: {d.get('father_name', 'N/A')}\n"
        f"🏠 Address: {d.get('address', 'N/A').replace('!', ' ')}\n"
        f"🌐 Circle: {d.get('circle', 'N/A')}\n"
        f"🆔 Aadhaar/ID: {d.get('id_number', 'N/A')}\n"
        f"📧 Email: {d.get('email', 'N/A')}\n"
        f"📞 Alternate Mobile: {d.get('alt_mobile', 'N/A')}\n"
    )

def send_long_text(chat_id, text):
    max_len = 4000
    if len(text) <= max_len:
        bot.send_message(chat_id, text)
    else:
        parts = [text[i:i + max_len] for i in range(0, len(text), max_len)]
        for part in parts:
            bot.send_message(chat_id, part)

def number_lookup(message):
    term = message.text.strip()
    if not term.isdigit() or len(term) != 10:
        bot.reply_to(message, "❌ Please enter a valid 10-digit mobile number (digits only).")
        return
    url = f"http://osintx.info/API/krobetahack.php?key=P6NW6D1&type=mobile&term={term}"
    try:
        res = requests.get(url, timeout=10).json()
        if isinstance(res, list) and res:
            results = [format_result(d, i + 1) for i, d in enumerate(res)]
            send_long_text(message.chat.id, "\n-----------------\n".join(results))
        else:
            bot.reply_to(message, f"❌ No data found for number `{term}`", parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Error: {e}")

def aadhaar_lookup(message):
    term = message.text.strip()
    if not term.isdigit() or len(term) != 12:
        bot.reply_to(message, "❌ Please enter a valid 12-digit Aadhaar/ID number (digits only).")
        return
    url = f"http://osintx.info/API/krobetahack.php?key=P6NW6D1&type=id_number&term={term}"
    try:
        res = requests.get(url, timeout=10).json()
        if isinstance(res, list) and res:
            results = [format_result(d, i + 1) for i, d in enumerate(res)]
            send_long_text(message.chat.id, "\n-----------------\n".join(results))
        else:
            bot.reply_to(message, f"❌ No data found for Aadhaar/ID `{term}`", parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Error: {e}")

print("🤖 Bot is running...")
bot.infinity_polling()
