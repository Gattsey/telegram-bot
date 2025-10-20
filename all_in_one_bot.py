import telebot

# ===== CONFIG =====
BOT_TOKEN = "B"     # your bot token from BotFather
OWNER_CHAT_ID = "O"            # your personal Telegram chat ID
GROUP_ID = "C"             # your group ID (starts with -100)
# ==================

bot = telebot.TeleBot(BOT_TOKEN)

# Handle screenshots (photos)
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        # Get username or name of sender
        username = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name

        # Highest quality photo
        photo = message.photo[-1].file_id

        # Send photo to your group with username in caption
        caption = f"📸 Screenshot from {username}"
        bot.send_photo(GROUP_ID, photo, caption=caption)

        # Tell sender it was sent successfully
        bot.reply_to(message, "✅ Screenshot received and sent successfully!")

        # Optional: notify you (the owner) privately
        bot.send_message(OWNER_CHAT_ID, f"📤 Screenshot received from {username}")

    except Exception as e:
        bot.reply_to(message, f"⚠️ Error: {e}")

# Handle /start command
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 Send me your screenshot and I’ll forward it to my owner!")

print("🤖 Bot is running... Press Ctrl + C to stop.")
bot.infinity_polling()

