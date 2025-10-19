import os
import telebot
import threading
from flask import Flask

# ====== LOAD ENVIRONMENT VARIABLES ======
TOKEN = os.getenv("BOT_TOKEN")
OWNER_CHAT_ID = int(os.getenv("OWNER_CHAT_ID"))
GROUP_CHAT_ID = int(os.getenv("GROUP_CHAT_ID"))

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ====== MESSAGE LINK TRACKER ======
# Store which private message maps to which group message
message_map = {}

# ====== START COMMAND ======
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 Welcome! Send a screenshot or message here to post it to your group.")

# ====== USER SENDS PHOTO ======
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        caption = f"📸 Screenshot from {message.from_user.first_name} (ID: {message.from_user.id})"
        sent = bot.send_photo(GROUP_CHAT_ID, message.photo[-1].file_id, caption=caption)
        bot.reply_to(message, "✅ Screenshot posted to your group.")
        message_map[message.message_id] = sent.message_id  # store mapping
    except Exception as e:
        bot.reply_to(message, f"⚠️ Error sending screenshot: {e}")

# ====== OWNER SENDS ANY MESSAGE ======
@bot.message_handler(func=lambda m: m.chat.id == OWNER_CHAT_ID,
                     content_types=['text', 'photo', 'video', 'document', 'animation'])
def send_to_group(message):
    try:
        if message.content_type == 'text':
            sent = bot.send_message(GROUP_CHAT_ID, message.text)
        elif message.content_type == 'photo':
            sent = bot.send_photo(GROUP_CHAT_ID, message.photo[-1].file_id, caption=(message.caption or ""))
        elif message.content_type == 'document':
            sent = bot.send_document(GROUP_CHAT_ID, message.document.file_id, caption=(message.caption or ""))
        elif message.content_type == 'video':
            sent = bot.send_video(GROUP_CHAT_ID, message.video.file_id, caption=(message.caption or ""))
        elif message.content_type == 'animation':
            sent = bot.send_animation(GROUP_CHAT_ID, message.animation.file_id, caption=(message.caption or ""))
        else:
            sent = bot.send_message(GROUP_CHAT_ID, "[Unsupported content type]")

        # store mapping between your private message and the group message
        message_map[message.message_id] = sent.message_id

        bot.send_message(OWNER_CHAT_ID, "📤 Message posted to your group (not forwarded).")
    except Exception as e:
        bot.send_message(OWNER_CHAT_ID, f"⚠️ Failed to post to group: {e}")

# ====== HEALTH CHECK ENDPOINT ======
@app.route("/")
def index():
    return "Bot is running fine!", 200

# ====== RUN THREADS ======
def run_flask():
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)

def run_bot():
    print("🤖 Bot is starting...")
    bot.infinity_polling()

if __name__ == "__main__":
    t = threading.Thread(target=run_bot, daemon=True)
    t.start()
    run_flask()

