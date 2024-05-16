import asyncio
import os
import sqlite3

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from write_to_exel import get_file


BOT_TOKEN = os.getenv("BOT_TOKEN")


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot)
    logging_middleware = LoggingMiddleware()
    dp.middleware.setup(logging_middleware)

    conn = sqlite3.connect('exchange_rates.db')
    cursor = conn.cursor()

    @dp.message_handler(commands=['start'])
    async def send_exchange_rate(message: types.Message):
        markup = types.ReplyKeyboardMarkup()
        info = types.KeyboardButton("/get_exchange_rate")

        markup.add(info)
        await message.answer("Для отримання інформації про курс долара використовуйте команду /get_exchange_rate",
                             reply_markup=markup)

    @dp.message_handler(commands=['get_exchange_rate'])
    async def get_exchange_rate(message: types.Message):
        file_path = await get_file()
        with open(file_path, 'rb') as file:
            await message.answer_document(file)

    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
