import telebot
from telebot import types

# 🔹 Твій токен бота
BOT_TOKEN = "ТВОЙ_ТОКЕН_БОТА"

# 🔹 ID адміна (кому приходять повідомлення)
ADMIN_ID = 8295534561

# 🔹 ID каналу (повинен починатися з мінуса!)
CHANNEL_ID = -1002361562441

bot = telebot.TeleBot(BOT_TOKEN)

# ✅ Коли користувач надсилає повідомлення
@bot.message_handler(func=lambda message: True, content_types=['text', 'photo', 'video', 'document'])
def handle_message(message):
    if message.from_user.id == ADMIN_ID:
        bot.send_message(ADMIN_ID, "⚠️ Ви не можете надсилати повідомлення самі собі.")
        return

    sender = message.from_user
    username = f"@{sender.username}" if sender.username else "Без ніка"
    sender_info = f"👤 Від: {sender.first_name}\n🔗 Профіль: {username}"

    # 🔘 Кнопки
    markup = types.InlineKeyboardMarkup()
    confirm_btn = types.InlineKeyboardButton("✅ Підтвердити", callback_data=f"confirm_{message.message_id}")
    cancel_btn = types.InlineKeyboardButton("❌ Відмінити", callback_data=f"cancel_{message.message_id}")
    markup.add(confirm_btn, cancel_btn)

    # Надсилаємо адміну
    if message.text:
        bot.send_message(ADMIN_ID, f"💬 Нове повідомлення:\n\n{message.text}", reply_markup=markup)
    else:
        bot.forward_message(ADMIN_ID, message.chat.id, message.message_id, protect_content=False)

    # Надсилаємо дані про відправника
    bot.send_message(ADMIN_ID, sender_info)

    # Відповідь користувачу
    bot.send_message(message.chat.id, "✅ Ваше повідомлення надіслано адміну на перевірку.")

# ✅ Обробка кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if not call.data.startswith(("confirm_", "cancel_")):
        return

    if call.message.chat.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "⛔ Тільки адміністратор може підтверджувати!")
        return

    action, msg_id = call.data.split("_")
    msg_id = int(msg_id)

    if action == "confirm":
        try:
            # Публікація в канал
            bot.send_message(CHANNEL_ID, f"📢 Повідомлення від користувача:\n\n{call.message.text}")
            bot.send_message(ADMIN_ID, "✅ Повідомлення надіслано в канал.")
        except Exception as e:
            bot.send_message(ADMIN_ID, f"⚠️ Помилка публікації: {e}")

    elif action == "cancel":
        bot.send_message(ADMIN_ID, "❌ Повідомлення скасовано.")

bot.polling(none_stop=True)
