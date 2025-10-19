import telebot
import os

# ====== CONFIGURATION ======
TOKEN = os.getenv("BOT_TOKEN")  # from Render Environment Variable
OWNER_CHAT_ID = 8288030589      # <-- replace with your chat ID
GROUP_ID = -1002759652647       # <-- replace with your group ID

bot = telebot.TeleBot(TOKEN)
last_message_id = None

# ====== START COMMAND ======
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 Welcome! Send a screenshot here to submit it.")

# ====== USER SENDS PHOTO (forward to owner) ======
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        # Forward photo to owner with user info
        caption = f"📸 Screenshot from {message.from_user.first_name} (ID: {message.from_user.id})"
        bot.send_photo(OWNER_CHAT_ID, message.photo[-1].file_id, caption=caption)
        bot.reply_to(message, "✅ Screenshot received!")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Error sending screenshot: {e}")

# ====== OWNER SENDS TO GROUP (no forwarded tag) ======
@bot.message_handler(func=lambda m: m.chat.id == OWNER_CHAT_ID,
                     content_types=['text', 'photo', 'video', 'document', 'animation'])
def send_to_group(message):
    global last_message_id
    try:
        if message.content_type == 'text':
            sent = bot.send_message(GROUP_ID, message.text)
        elif message.content_type == 'photo':
            sent = bot.send_photo(GROUP_ID, message.photo[-1].file_id, caption=(message.caption or ""))
        elif message.content_type == 'document':
            sent = bot.send_document(GROUP_ID, message.document.file_id, caption=(message.caption or ""))
        elif message.content_type == 'video':
            sent = bot.send_video(GROUP_ID, message.video.file_id, caption=(message.caption or ""))
        elif message.content_type == 'animation':
            sent = bot.send_animation(GROUP_ID, message.animation.file_id, caption=(message.caption or ""))
        else:
            sent = bot.send_message(GROUP_ID, "[Unsupported content type]")
        last_message_id = sent.message_id
        bot.send_message(OWNER_CHAT_ID, "📤 Message posted to your group (not forwarded).")
    except Exception as e:
        bot.send_message(OWNER_CHAT_ID, f"⚠️ Failed to post to group: {e}")

# ====== PIN COMMAND ======
@bot.message_handler(commands=['pin'])
def pin_message(message):
    try:
        if message.chat.type in ['group', 'supergroup']:
            if message.reply_to_message:
                bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id)
                bot.reply_to(message, "📌 Message pinned successfully!")
            else:
                bot.reply_to(message, "Reply to a message and then use /pin.")
        else:
            bot.reply_to(message, "This command works only in groups.")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Failed to pin message: {e}")

# ====== RUN ======
print("🤖 Bot is running...")
bot.infinity_polling()

