from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
import subprocess

bot_token = '6858480572:AAGUJwUq_UevIhrbQS6cG2nN0hfyDw8yh54'
chat_id = '-4134676016'  # ID вашего чата или пользователя, которому вы хотите отправлять результаты

bot = Bot(token=bot_token)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот, который может запускать вашу программу. "
                        "Используйте команду /run для запуска программы.")

@dp.message_handler(commands=['run'])
async def run_program(message: types.Message):
    output = subprocess.check_output(['python', 'my_program.py'])
    await bot.send_message(chat_id, output, parse_mode=ParseMode.HTML)

if __name__ == '__main__':
    dp.start_polling()