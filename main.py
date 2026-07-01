from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart
import asyncio
import os

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "👋 ¡Hola!\n\n"
        "Envíame un enlace de TikTok o Facebook y descargaré el video."
    )


@dp.message(F.text)
async def downloader(message: Message):
    await message.answer(
        "⏳ Procesando tu enlace...\n(Esta función la agregaremos en el siguiente paso)."
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
