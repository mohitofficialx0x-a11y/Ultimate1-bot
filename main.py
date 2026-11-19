import os
import re
import threading
import requests
import telebot
from flask import Flask
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "9233333873:AAER-zBuyTHBxEc0EellZ4Zda9fJJWGxWYE"
CHANNEL_URL = "https://t.me/+UyBmDcQRKORlNGI1"
CHANNEL_CHAT_ID = -1004383355739
GUIDE_VIEWER_URL = "https://ibb.co/Q7w4QQXh"
LOCAL_IMAGE_PATH = "guide.png"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)


@app.route("/")
def home():
    return "MOHIT FZX Bot is running!", 200


def get_direct_image_url(viewer_url: str):
    try:
        resp = requests.get(viewer_url, timeout=15)
        resp.raise_for_status()
        match = re.search(r"https://i\.ibb\.co/[A-Za-z0-9_-]+/[^\s\"'<>]+", resp.text)
        if match:
            return match.group(0)
    except Exception as e:
        print(f"Viewer page fetch error: {e}")
    return None


def send_tutorial_photo(chat_id: int):
    caption = "📸 *HOW TO JOIN & VERIFY*\nStep 1: Channel join karein\nStep 2: *I HAVE JOINED* dabayein 👇"

    if os.path.exists(LOCAL_IMAGE_PATH):
        with open(LOCAL_IMAGE_PATH, "rb") as img:
            bot.send_photo(chat_id, img, caption=caption, parse_mode="Markdown")
        return True

    direct_url = get_direct_image_url(GUIDE_VIEWER_URL)
    if direct_url:
        try:
            img_resp = requests.get(direct_url, timeout=15)
            img_resp.raise_for_status()
            bot.send_photo(chat_id, img_resp.content, caption=caption, parse_mode="Markdown")
            return True
        except Exception as e:
            print(f"Direct image send error: {e}")

    return False


def is_user_joined(user_id: int) -> bool:
    try:
        member = bot.get_chat_member(CHANNEL_CHAT_ID, user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        print(f"Force join check error: {e}")
        return False


def send_force_join_screen(chat_id: int, include_photo: bool = True):
    if include_photo:
        send_tutorial_photo(chat_id)

    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("📢 JOIN OUR CHANNEL", url=CHANNEL_URL))
    markup.add(InlineKeyboardButton("✅ I HAVE JOINED", callback_data="/claim"))

    text = (
        "🔥 *WELCOME TO MOHIT FZX BOT* 🔥\n\n"
        "📢 Is bot ko use karne ke liye aapko hamara official channel join karna zaroori hai!\n\n"
        "👇 Niche diye gaye button par click karke channel join karein:"
    )

    bot.send_message(
        chat_id,
        text,
        parse_mode="Markdown",
        reply_markup=markup,
        disable_web_page_preview=True
    )


def send_main_menu(chat_id: int):
    text = (
        "👑 *WELCOME TO MOHIT FZX* 👑\n\n"
        "🔥 नमस्कार! आपका हमारे Telegram Account पर स्वागत है। ❤️\n\n"
        "🚀 यहाँ आपको मिलेंगे हमारे सभी जरूरी Gaming & Earning Bots एक ही जगह पर।\n\n"
        "💡 *New Offer:* OTP Panel ke liye type karein ➡️ /otp or /start\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "📲 नीचे दिए गए बटन पर क्लिक करें:\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "👤 *Admin / Contact:* @FZXMOHIT1\n"
        "💬 Need help? Type /contact\n\n"
        "⚡ Fast Service | 24×7 Support\n"
        "💀 POWERED BY MOHIT™ 🚀"
    )

    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("🚨 NEED OTP PANEL? CLICK HERE", url="https://t.me/Unlimited_otp_s_bot"),
        InlineKeyboardButton("🚀🎮 P77 Game Bot", url="https://t.me/P77Game_bot?start=ref8472943262"),
        InlineKeyboardButton("💥🎮 Official 5222 Bot", url="https://t.me/Official_5222_bot?start=ref8472943262"),
        InlineKeyboardButton("🥶🎮 Benzc Game Bot", url="https://t.me/benzcgame_bot?start=ref8472943262"),
        InlineKeyboardButton("❌🎮 X89", url="https://t.me/x89com_bot?start=ref8472943262"),
        InlineKeyboardButton("💥🚀TRICK", callback_data="/TRICK"),
        InlineKeyboardButton("💀🎮 AA GAME Official", url="https://t.me/AAGAMEofficial_bot?start=8472943262"),
        InlineKeyboardButton("🥰🎮 Seven7BET Official", url="https://t.me/Seven7BETOfficial_bot?start=8472943262"),
        InlineKeyboardButton("💸🎮 MPL GAME Official", url="https://t.me/MPLGAMEofficial_bot?start=8472943262"),
        InlineKeyboardButton("☠️🎮 Topone Official", url="https://t.me/ToponeOfficial_bot?start=8472943262"),
        InlineKeyboardButton("📖🎬 Tutorial", callback_data="/tutorial"),
        InlineKeyboardButton("🙋💬 Contact Admin", callback_data="/contact")
    )

    bot.send_message(
        chat_id,
        text,
        parse_mode="Markdown",
        reply_markup=markup,
        disable_web_page_preview=True
    )


def send_contact_menu(chat_id: int):
    text = (
        "👋 Hello Bhai! Are you trying to contact me? 🤔💬\n\n"
        "Agar koi dikkat ya query hai, toh seedha niche diye gaye button par click karke mujhe message karo! 🚀🔥\n\n"
        "👤 *Official Admin:* @FZXMOHIT1"
    )
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("📩 Message Admin Now", url="https://t.me/FZXMOHIT1"))
    bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=markup)


def send_otp_menu(chat_id: int):
    text = (
        "⚡ *UNLIMITED OTP PANEL HUB* ⚡\n\n"
        "🔥 Bhai, agar tujhe non-stop aur fast OTPs chahiye toh niche diye gaye button par click karke seedha hamare official OTP bot par jao!\n\n"
        "📌 *Bot Details:*\n"
        "• Fast & Instant Delivery 🚀\n"
        "• 24×7 Active Service 🟢\n"
        "• Trusted by All Users 💯\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "👇 *Click Below to Open Panel:*"
    )
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("🚀 OPEN UNLIMITED OTP PANEL", url="https://t.me/Unlimited_otp_s_bot"),
        InlineKeyboardButton("🔙 Back to Main Menu", callback_data="/start")
    )
    bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=markup)


@bot.message_handler(commands=["start"])
def handle_start(message):
    if is_user_joined(message.from_user.id):
        send_main_menu(message.chat.id)
    else:
        send_force_join_screen(message.chat.id, include_photo=True)


@bot.message_handler(commands=["contact"])
def handle_contact(message):
    if not is_user_joined(message.from_user.id):
        send_force_join_screen(message.chat.id, include_photo=False)
        return
    send_contact_menu(message.chat.id)


@bot.message_handler(commands=["otp"])
def handle_otp(message):
    if not is_user_joined(message.from_user.id):
        send_force_join_screen(message.chat.id, include_photo=False)
        return
    send_otp_menu(message.chat.id)


@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    data = call.data
    user_id = call.from_user.id
    chat_id = call.message.chat.id

    if data == "/claim":
        if is_user_joined(user_id):
            bot.answer_callback_query(call.id, "✅ Verified! Welcome!")
            send_main_menu(chat_id)
        else:
            bot.answer_callback_query(call.id, "❌ Pehle channel join karo!", show_alert=True)
            send_force_join_screen(chat_id, include_photo=False)
        return

    if not is_user_joined(user_id):
        bot.answer_callback_query(call.id, "❌ Pehle channel join karo!", show_alert=True)
        send_force_join_screen(chat_id, include_photo=False)
        return

    if data == "/start":
        bot.answer_callback_query(call.id)
        send_main_menu(chat_id)
    elif data == "/contact":
        bot.answer_callback_query(call.id)
        send_contact_menu(chat_id)
    elif data == "/TRICK":
        bot.answer_callback_query(call.id)
        bot.send_message(
            chat_id,
            "💥🚀 *TRICKS SECTION*\n\nYahan apni tricks ka message/content add kar le bhai!",
            parse_mode="Markdown"
        )
    elif data == "/tutorial":
        bot.answer_callback_query(call.id)
        send_tutorial_photo(chat_id)


def run_bot():
    print("MOHIT FZX Bot polling started...")
    bot.infinity_polling(skip_pending=True)


threading.Thread(target=run_bot, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
