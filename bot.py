import json
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv
import os

load_dotenv()

# -----------------------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
# -----------------------------

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Открыть магазин",
            web_app=WebAppInfo(url="https://shop-mini-app-git-master-roms-projects-d8509921.vercel.app/")
        )]
    ])
    await message.answer("Добро пожаловать! Нажмите кнопку ниже:", reply_markup=kb)

@dp.message(lambda m: m.web_app_data is not None)
async def handle_webapp(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        product = data.get("product", "Неизвестно")
        qty = data.get("quantity", 1)
        comment = data.get("comment", "")
        username = data.get("username") or "—"
        user_id = data.get("user_id") or message.from_user.id

        text = (
            f"🛒 <b>Новый заказ!</b>\n"
            f"<b>Товар:</b> {product}\n"
            f"<b>Количество:</b> {qty}\n"
            f"<b>Комментарий:</b> {comment or '—'}\n"
            f"<b>Пользователь:</b> @{username}\n"
            f"<b>ID:</b> <code>{user_id}</code>"
        )
        await bot.send_message(ADMIN_ID, text)
        await message.answer(f"✅ Заказ на {product} отправлен! Мы скоро свяжемся.")
    except Exception as e:
        logging.error(e)
        await message.answer("⚠️ Ошибка при обработке заказа.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
