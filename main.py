import qrcode
from io import BytesIO
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import BufferedInputFile
import asyncio

TOKEN = "8387546130:AAGltnPBd9Kw9vpsL80oz4XddUaHLoQ29mk"
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        "Salom! 👋\nMenga matn, fayl, rasm yoki video yuboring — men sizga QR kod yasab beraman 📱"
    )


# --- Universal QR yasovchi funksiya ---
async def send_qr(message: types.Message, data: str, caption: str):
    qr = qrcode.make(data)
    bio = BytesIO()
    qr.save(bio, format="PNG")
    bio.seek(0)
    photo = BufferedInputFile(bio.read(), filename="qr.png")
    await message.answer_photo(photo=photo, caption=caption)


# Matndan QR kod
@dp.message(F.text)
async def make_qr_from_text(message: types.Message):
    await send_qr(message, message.text, "✅ Sizning QR kodingiz!")


# Rasm uchun
@dp.message(F.photo)
async def make_qr_from_photo(message: types.Message):
    file = await bot.get_file(message.photo[-1].file_id)
    file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file.file_path}"
    await send_qr(message, file_url, "📸 Rasm QR kodingiz tayyor!")


# Fayl uchun
@dp.message(F.document)
async def make_qr_from_file(message: types.Message):
    file = await bot.get_file(message.document.file_id)
    file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file.file_path}"
    await send_qr(message, file_url, "📁 Fayl QR kodingiz tayyor!")


# Video uchun
@dp.message(F.video)
async def make_qr_from_video(message: types.Message):
    file = await bot.get_file(message.video.file_id)
    file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file.file_path}"
    await send_qr(message, file_url, "🎥 Video QR kodingiz tayyor!")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
