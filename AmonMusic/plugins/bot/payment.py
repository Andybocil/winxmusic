from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InputMediaPhoto
from AmonMusic import app
# URL atau Path gambar yang ingin ditampilkan
PHOTO_URL = "https://telegra.ph/file/5c656925faa3d0265f640.jpg"  # Ganti dengan foto yang diinginkan

# Data daftar jasa dan pembayaran
class Data:
    JASA = """
<b>DAFTAR JASA BOT:</b>

1. Pembuatan Bot Menfess
   Deskripsi: Bot untuk mengelola layanan postingan anonim (menfess) di grup.
   Fitur:
   - Menfess dalam grup dengan anonim.
   - Tampilan yang menarik dan mudah digunakan.
   - Pengaturan batas waktu menfess.
   - Dukungan berbagai perintah kustom.
   - Integrasi dengan database.

2. Pembuatan Bot Music
   Deskripsi: Bot untuk memutar musik di grup atau saluran.
   Fitur:
   - Memutar musik dari YouTube dan platform lainnya.
   - Kontrol musik lengkap (play, pause, skip, dll.).
   - Tampilan informasi musik yang sedang diputar.
   - Dukungan daftar putar.
   - Integrasi dengan database.

3. Pembuatan Bot File Sharing (Fsub Telegram)
   Deskripsi: Bot untuk menyimpan dan berbagi file melalui tautan khusus.
   Fitur:
   - Mengunggah file ke bot dan mendapatkan tautan unik.
   - Mengelola file yang diunggah (menghapus, dll.).
   - Tampilan statistik unduhan file.
   - Dukungan untuk berbagai jenis file.

Untuk informasi lebih lanjut dan pemesanan, silakan hubungi @OwnNeko.
"""

    DANA = """
DANA : 081398871823
"""

    QRIS = """
Klik Disini </b><a href='https://telegra.ph/file/3a8701cb42f9af1483800.jpg'>QRIS BrotherCloth</a>
"""

    # Tombol utama
    main_buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🛒 JASA", callback_data="jasa"),
            InlineKeyboardButton("💰 DANA", callback_data="dana"),
            InlineKeyboardButton("💳 QRIS", callback_data="qris"),
        ],
        [
            InlineKeyboardButton("❌ ᴛᴜᴛᴜᴘ", callback_data="close")
        ]
    ])

    # Tombol kembali
    back_button = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Kembali", callback_data="back")],
    ])




# Handler untuk memulai bot dan menampilkan foto + tombol utama
@app.on_message(filters.command("pay"))
def start(client, message):
    client.send_photo(
        chat_id=message.chat.id,
        photo=PHOTO_URL,
        caption="Selamat datang Di MEMEX PROJECT! Pilih menu di bawah ini untuk mengetahui jasa dan sistem pembayaran:",
        reply_markup=Data.main_buttons
    )


# Handler untuk callback "jasa"
@app.on_callback_query(filters.regex("^jasa$"))
def jasa_callback(client, query: CallbackQuery):
    query.message.edit_text(
        text=Data.JASA,
        reply_markup=Data.back_button,
        disable_web_page_preview=True
    )


# Handler untuk callback "dana"
@app.on_callback_query(filters.regex("^dana$"))
def dana_callback(client, query: CallbackQuery):
    query.message.edit_text(
        text=Data.DANA,
        reply_markup=Data.back_button
    )


# Handler untuk callback "qris"
@app.on_callback_query(filters.regex("^qris$"))
def qris_callback(client, query: CallbackQuery):
    query.message.edit_text(
        text=Data.QRIS,
        reply_markup=Data.back_button,
        disable_web_page_preview=True
    )


# Handler untuk tombol kembali ke menu utama
@app.on_callback_query(filters.regex("^back$"))
def back_callback(client, query: CallbackQuery):
    query.message.edit_media(
        media=InputMediaPhoto(
            media=PHOTO_URL,
            caption="Selamat datang! Pilih menu di bawah ini:"
        ),
        reply_markup=Data.main_buttons
    )


# Handler untuk callback "close" (menutup pesan)
@app.on_callback_query(filters.regex("^close$"))
def close_callback(client, query: CallbackQuery):
    query.message.delete()


