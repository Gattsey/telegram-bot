import os
import telebot

TOKEN = os.getenv("BOT_TOKEN")
OWNER_CHAT_ID = int(os.getenv("OWNER_CHAT_ID"))
GROUP_ID = int(os.getenv("GROUP_ID"))

bot = telebot.TeleBot(TOKEN)
last_message_id = None

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 Welcome! Send a screenshot here to submit it.")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        caption = f"📸 Screenshot from {message.from_user.first_name} (ID: {message.from_user.id})"
        bot.send_photo(OWNER_CHAT_ID, message.photo[-1].file_id, caption=caption)
        bot.reply_to(message, "✅ Screenshot received!")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Error sending screenshot: {e}")

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

print("🤖 Bot is running...")
bot.infinity_polling()

