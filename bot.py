import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiohttp import web

# Загружаем переменные из .env
load_dotenv(dotenv_path = "/home/pcrom/Рабочий стол/shop-mini-bot/.env")

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # URL для webhook (в Vercel это будет динамическая ссылка)

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN не найден в окружении. Проверьте файл .env")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я бот с webhook.")

# Обработчик текста — эхо (показывает как принимать обычные сообщения)
@dp.message()
async def echo_message(message: types.Message):
    await message.answer(f"Ты написал: {message.text}")

# Активация webhook (переход на URL)
async def on_start(request):
    return web.Response(text="Webhook активирован!")

# Основная функция для обработки webhook
async def on_webhook(request):
    json_data = await request.json()
    update = types.Update(**json_data)
    await dp.process_update(update)
    return web.Response()

# Основной сервер aiohttp
async def on_shutdown(app):
    await bot.session.close()

# Функция для запуска webhook
async def set_webhook():
    webhook_info = await bot.set_webhook(WEBHOOK_URL)
    print("Webhook URL установлен:", webhook_info.url)

# Создание серверного приложения и запуск
def run_webhook():
    app = web.Application()
    app.router.add_get('/', on_start)  # Обработчик главной страницы
    app.router.add_post(f'/{BOT_TOKEN}', on_webhook)  # Обработчик webhook запросов
    app.on_shutdown.append(on_shutdown)
    web.run_app(app, port=8000)

if __name__ == "__main__":
    import asyncio
    asyncio.run(set_webhook())  # Устанавливаем webhook URL
    run_webhook()  # Запускаем сервер
