from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from AmonMusic import app

class Data:
    JASA = """
<b>DAFTAR:</b>
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
Untuk informasi lebih lanjut dan pemesanan, silakan hubungi @ownercpkoid.
"""

    DANA = """
    <b>💳 ᴍᴏᴛᴏᴅᴇ ᴘᴇᴍʙᴀʏᴀʀᴀɴ:</b>
    <b>├ ᴅᴀɴᴀ</b>
    <b>└────• <code>0895340192141</code></b>
    """
    
    QRIS = """📌 *Scan QRIS untuk pembayaran:*
    
Klik 👉 <a href='https://files.catbox.moe/oi9hrz.jpg'>QRIS MemexProject</a>"""

    MENU_IMAGE = "https://telegra.ph/file/5c656925faa3d0265f640.jpg"

    main_buttons = [
        [
            InlineKeyboardButton("🛒 JASA", callback_data="jasa"),
            InlineKeyboardButton("📇 QRIS", callback_data="qris"),
            InlineKeyboardButton("💳 DANA", callback_data="dana"),
        ],
        [InlineKeyboardButton("🏘 Menu", callback_data=f"settingsback_helper")],
        [InlineKeyboardButton("❌ Tutup", callback_data="close")]
    ]

    submenu_buttons = [
        [InlineKeyboardButton("🔙 Kembali", callback_data="pay")],
        [InlineKeyboardButton("❌ Tutup", callback_data="close")]
    ]

@app.on_message(filters.command("pay"))
async def menu(_, msg):
    buttons = InlineKeyboardMarkup(Data.main_buttons)
    
    await msg.reply_photo(
        photo=Data.MENU_IMAGE,
        caption="📌 *Pilih layanan yang tersedia:*",
        reply_markup=buttons
    )

@app.on_callback_query(filters.regex("pay"))
async def kembali_callback(_, query):
    buttons = InlineKeyboardMarkup(Data.main_buttons)
    
    await query.message.edit_media(
        InputMediaPhoto(
            media=Data.MENU_IMAGE,
            caption="📌 *Pilih layanan yang tersedia:*"
        ),
        reply_markup=buttons
    )

@app.on_callback_query(filters.regex("jasa"))
async def jasa_callback(_, query):
    buttons = InlineKeyboardMarkup(Data.submenu_buttons)
    
    await query.message.edit_text(
        Data.JASA,
        reply_markup=buttons,
        disable_web_page_preview=True
    )

@app.on_callback_query(filters.regex("dana"))
async def dana_callback(_, query):
    buttons = InlineKeyboardMarkup(Data.submenu_buttons)
    
    await query.message.edit_text(
        Data.DANA,
        reply_markup=buttons
    )

@app.on_callback_query(filters.regex("qris"))
async def qris_callback(_, query):
    buttons = InlineKeyboardMarkup(Data.submenu_buttons)
    
    await query.message.edit_text(
        Data.QRIS,
        reply_markup=buttons,
        disable_web_page_preview=True
    )

@app.on_callback_query(filters.regex("close"))
async def close_callback(_, query):
    await query.message.delete()
