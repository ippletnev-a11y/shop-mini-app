import os
import json
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
import asyncio
import uvicorn
from dotenv import load_dotenv


load_dotenv()

# === Конфигурация ===
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher()

# === Создаем FastAPI для приёма JSON от Mini App ===
app = FastAPI()

# Пример эндпоинта, куда Mini App будет отправлять JSON
@app.post("/data")
async def receive_data(request: Request):
    data = await request.json()  # Читаем JSON из запроса
    print("📩 Получен JSON:", data)

    # Например, отправим данные тебе в Telegram
    chat_id = 1986051958  # Подставь свой chat_id
    text = f"📦 Получен заказ из Mini App:\n\n{json.dumps(data, indent=2, ensure_ascii=False)}"
    await bot.send_message(chat_id, text)

    return {"status": "ok", "message": "JSON получен!"}

# === Пример обычного хэндлера Telegram ===
@dp.message()
async def echo_message(message: Message):
    await message.answer("Привет! Я готов принимать JSON от твоей Mini App 🚀")

# === Основная функция ===
async def main():
    # Запускаем aiogram и FastAPI одновременно
    loop = asyncio.get_running_loop()

    # Запускаем FastAPI (в фоне)
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)

    # Запускаем бота и сервер параллельно
    await asyncio.gather(
        dp.start_polling(bot),
        server.serve()
    )

if __name__ == "__main__":
    asyncio.run(main())
