import os
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from downloader import download_video

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("No se encontró la variable BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "🎥 *TikFace*\n\n"
        "Envíame un enlace de TikTok o Facebook y te enviaré el video.",
        parse_mode="Markdown",
    )


@dp.message(F.text)
async def handle_link(message: Message):
    url = message.text.strip()

    if "tiktok.com" not in url and "facebook.com" not in url and "fb.watch" not in url:
        await message.answer("❌ Solo acepto enlaces de TikTok o Facebook.")
        return

    status = await message.answer("⏳ Descargando video...")

    loop = asyncio.get_running_loop()
    file_path = await loop.run_in_executor(None, download_video, url)

    if not file_path:
        await status.edit_text("❌ No pude descargar ese video.")
        return

    try:
        video = FSInputFile(file_path)
        await message.answer_video(video)
        await status.delete()
    except Exception:
        await status.edit_text("❌ Ocurrió un error al enviar el video.")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
