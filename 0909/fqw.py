from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()
bot_token = os.getenv("BOT_TOKEN")

dp = Dispatcher()


@dp.message(Command("start"))
async def command_start(message: Message):
    await message.answer("Hello!")

@dp.message()
async def norm_mess(message:Message):
    await message.answer("repeat")

async def main():
    bot = Bot(token=bot_token)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
          