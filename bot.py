import json
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.session.aiohttp import AiohttpSession
import asyncio

# ------------------------------------------------------------
# 🔧 Настройки
# ------------------------------------------------------------
BOT_TOKEN = "8248066160:AAFFs98RKdSLYoCH9-RtbZi-QD0oERf9tcM"   # замените на токен от @BotFather
ADMIN_ID = 1986051958            # замените на свой Telegram ID

# ------------------------------------------------------------
# 🔧 Логирование
# ------------------------------------------------------------
logging.basicConfig(level=logging.INFO)

# ------------------------------------------------------------
# 🔧 Инициализация
# ------------------------------------------------------------
session = AiohttpSession()
bot = Bot(token=BOT_TOKEN, session=session, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# ------------------------------------------------------------
# 🏪 Команда /start
# ------------------------------------------------------------
@dp.message(CommandStart())
async def start(message: types.Message):
    """Отправляем пользователю кнопку для открытия Mini App"""
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Открыть магазин",
            web_app=WebAppInfo(url="https://shop-mini-app-eight.vercel.app/mini_app")
        )]
    ])
    await message.answer(
        "Добро пожаловать в магазин свечей 🕯️\n\n"
        "Нажмите кнопку ниже, чтобы открыть Mini App.",
        reply_markup=kb
    )

# ------------------------------------------------------------
# 🧾 Обработка данных из Mini App
# ------------------------------------------------------------
@dp.message(lambda m: m.web_app_data is not None)
async def handle_webapp_data(message: types.Message):
    """Принимаем данные, отправленные из Mini App (tg.sendData)"""
    try:
        data = json.loads(message.web_app_data.data)
        product = data.get("product", "Неизвестно")
        qty = data.get("quantity", 1)
        comment = data.get("comment", "")
        username = data.get("username") or "—"
        user_id = data.get("user_id") or message.from_user.id

        # Сообщение для администратора
        admin_text = (
            f"<b>🛒 Новый заказ из Mini App</b>\n\n"
            f"<b>Товар:</b> {product}\n"
            f"<b>Кол-во:</b> {qty}\n"
            f"<b>Комментарий:</b> {comment or '—'}\n\n"
            f"<b>Пользователь:</b> @{username}\n"
            f"<b>ID:</b> <code>{user_id}</code>"
        )
        await bot.send_message(ADMIN_ID, admin_text)

        # Ответ пользователю
        await message.answer(
            f"✅ Спасибо за заказ!\n\n"
            f"Товар: <b>{product}</b>\n"
            f"Количество: <b>{qty}</b>\n"
            f"Мы скоро с вами свяжемся 💬"
        )

    except Exception as e:
        logging.error(f"Ошибка обработки данных Mini App: {e}")
        await message.answer("⚠️ Ошибка при обработке данных. Попробуйте снова.")

# ------------------------------------------------------------
# 🚀 Запуск
# ------------------------------------------------------------
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
