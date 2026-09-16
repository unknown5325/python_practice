import asyncio
import telethon
import keyring
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import events
from datetime import datetime, timedelta



API_ID = ''
API_TOKEN = ''
session_name = ''
targets = [-1001007302005, '@Wylsared']
chats = 207749386

client = telethon.TelegramClient(session_name, API_ID, API_TOKEN)
@client.on(events.NewMessage(chats=targets))
async def all():
    soo = await client.get_entity(targets[0])
    async for msg in client.iter_messages(soo, limit=10):
        #if event.date > datetime.now(event.date.tzinfo) - timedelta(days=1):
        if 'iphone' in msg.text.lower():
            await msg.forwards_to(chats)
            print('Сообщение получено из чата: ', msg.chat.title)
            print(msg.text)
            print(msg.date)
    await client.disconnect()


async def main():
    await client.start()
    print('Запушено')

if __name__ == "__main__":
    asyncio.run(main())