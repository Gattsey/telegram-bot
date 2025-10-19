import telebot

# === Replace these ===
TOKEN = "8289102024:AAEPXj4CSu6wdZdJcBbMtBDc9jr1RoLaCo8"        # 👈 your bot token from BotFather
OWNER_CHAT_ID = 8288030589            # 👈 your chat ID (you got earlier)
GROUP_ID = -1002759652647            # 👈 your group/channel ID

bot = telebot.TeleBot(TOKEN)
last_message_id = None  # remember the last message sent to group


# --- /start command ---
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "👋 Hi! Please send your screenshot or message here.")


# --- Handle photos from anyone ---
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    # Forward to owner
    bot.forward_message(OWNER_CHAT_ID, message.chat.id, message.message_id)

    # Notify owner
    bot.send_message(OWNER_CHAT_ID, f"📸 Screenshot received from user ID: {message.chat.id}")

    # Thank the user
    bot.send_message(message.chat.id, "✅ Thanks! Your screenshot has been sent successfully!")


# --- Handle messages from OWNER (send to group) ---
@bot.message_handler(func=lambda m: m.chat.id == OWNER_CHAT_ID,
                     content_types=['text', 'photo', 'video', 'document', 'animation'])
def send_to_group(message):
    global last_message_id

    # Forward message from owner to group
    sent = bot.forward_message(GROUP_ID, message.chat.id, message.message_id)
    last_message_id = sent.message_id  # save last sent message ID

    bot.send_message(OWNER_CHAT_ID, "📤 Message sent to your group successfully!")


# --- /pin command (pin the last sent message) ---
@bot.message_handler(commands=['pin'])
def pin_message(message):
    global last_message_id
    if message.chat.id != OWNER_CHAT_ID:
        bot.send_message(message.chat.id, "❌ You’re not allowed to use this command.")
        return

    if last_message_id:
        bot.pin_chat_message(GROUP_ID, last_message_id)
        bot.send_message(OWNER_CHAT_ID, "📌 Last message pinned successfully!")
    else:
        bot.send_message(OWNER_CHAT_ID, "⚠️ No message to pin yet!")


print("🤖 Bot is running... Press Ctrl + C to stop.")
bot.infinity_polling()
