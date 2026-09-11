import httpx
import warnings
import urllib3
import logging



# 1. Monkey-patch httpx: заставляем ВСЕ AsyncClient использовать verify=False
_original_async_init = httpx.AsyncClient.__init__
_original_sync_init = httpx.Client.__init__

def _patched_async_init(self, *args, **kwargs):
    kwargs['verify'] = False
    return _original_async_init(self, *args, **kwargs)

def _patched_sync_init(self, *args, **kwargs):
    kwargs['verify'] = False
    return _original_sync_init(self, *args, **kwargs)

httpx.AsyncClient.__init__ = _patched_async_init
httpx.Client.__init__ = _patched_sync_init

# 2. Отключаем спам предупреждений о небезопасном соединении
warnings.filterwarnings('ignore', message='Unverified HTTPS request')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("httpcore").setLevel(logging.ERROR)



import csv
import requests
from io import StringIO
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import os
import httpx
from telegram import Bot
from telegram.ext import ApplicationBuilder



load_dotenv()
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")

# ==== ФУНКЦИИ ДЛЯ API ====
def get_weather():
    # Бесплатный API wttr.in
    url = f"https://wttr.in/Minsk?format=j1"
    r = requests.get(url).json()
    forecast = []
    for day in r["weather"]:
        date = day["date"]
        avgtemp = day["avgtempC"]
        desc = day["hourly"][4]["weatherDesc"][0]["value"]
        forecast.append(f"{date}: {avgtemp}°C, {desc}")
    return "\n".join(forecast)


def get_stock_price():
    # Пример: MSFT.US — Microsoft, AAPL.US — Apple
    ticker = "MSFT.US"
    url = f"https://stooq.com/q/l/?s={ticker}&f=sd2t2ohlcv&h&e=csv"
    r = requests.get(url)
    r.encoding = "utf-8"
    data = list(csv.DictReader(StringIO(r.text)))
    if data and "Close" in data[0]:
        price = data[0]["Close"]
        return f"Цена акции {ticker}: {price} USD"
    else:
        return "Не удалось получить данные по акции."

def get_btc_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    r = requests.get(url).json()
    price = r["bitcoin"]["usd"]
    return f"Bitcoin: {price} USD"

def get_ip():
    url = 'https://api.ipify.org?format=json'
    r = requests.get(url).json()
    return r

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [("Погода","Акция","Валюта", "Ip")]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('Привет! Выбирете действие:', reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if  text == "погода":
        await update.message.reply_text(get_weather())
    elif  text == "акция":
        await update.message.reply_text(get_stock_price())
    elif  text == "валюта":
        await update.message.reply_text(get_btc_price())
    elif  text == "ip":
        await update.message.reply_text(get_ip())
    else:
        await update.message.reply_text('Не понял команду. Выберите из меню: ')
        await update.message.reply_audio(audio='', caption='трек', title='название трека', performer='исполнитель')
        await update.message.reply_video(video='', supports_streaming=True)
        await update.message.reply_photo(photo='', caption='')
        await update.message.reply_document(document='', caption='')

        new_keyboard = ['fds']
        reply_markup = ReplyKeyboardMarkup(keyboard=new_keyboard, resize_keyboard=True)
        await update.message.edit_reply_markup(reply_markup=reply_markup)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()