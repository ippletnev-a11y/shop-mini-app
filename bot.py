# bot.py
import asyncio                     # для запуска асинхронного цикла
import os                          # для чтения переменных окружения
from dotenv import load_dotenv     # читает .env файл
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# Загружаем переменные из .env в окружение (os.getenv)
load_dotenv()

# Получаем токен бота
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN не найден в окружении. Проверьте файл .env")

# Инициализация объектов aiogram
bot = Bot(token=BOT_TOKEN)   # объект для взаимодействия с Telegram API
dp = Dispatcher()            # диспетчер — регистрирует обработчики сообщений/команд

# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """
    Отправляет приветствие пользователю при вводе /start.
    message: объект с информацией о сообщении и пользователе
    """
    await message.answer(
        "Привет! Я тестовый бот для Mini App.\n"
        "Напиши /app чтобы получить кнопку открытия Mini App."
    )

# Обработчик команды /app — показывает inline-кнопку с web_app (Mini App)
@dp.message(Command("app"))
async def cmd_app(message: types.Message):
    """
    Отправляет инлайн-кнопку, открывающую Mini App (веб-страницу).
    Замените url на свой хостинг (например https://your-domain.com).
    """
    # WebAppInfo указывает URL, который откроется внутри Telegram
    webapp_url = "https://shop-mini-app-eight.vercel.app/"  # <- замените на реальный URL вашего Mini App
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Открыть Mini App", web_app=WebAppInfo(url=webapp_url))]
    ])
    await message.answer("Нажми кнопку ниже, чтобы открыть Mini App:", reply_markup=keyboard)

# Обработчик текста — эхо (показывает как принимать обычные сообщения)
@dp.message()
async def echo_message(message: types.Message):
    """
    Эхо-обработчик: возвращает текст обратно пользователю.
    Полезен для тестирования, что бот живой.
    """
    await message.answer(f"Ты написал: {message.text}")

# Запуск polling (в режиме разработки проще всего)
async def main():
    """
    Запускаем long polling. В продакшене можно настроить webhook.
    """
    try:
        print("Запуск бота...")
        await dp.start_polling(bot)
    finally:
        # Гарантируем корректное закрытие сессии HTTP клиента aiogram
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
