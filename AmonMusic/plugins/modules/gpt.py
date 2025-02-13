import nest_asyncio
nest_asyncio.apply()

import os
from gtts import gTTS
import requests
from pyrogram import filters
from pyrogram.enums import ChatAction, ParseMode  # Pastikan ParseMode diimpor
from AmonMusic import app  # Sesuaikan dengan struktur bot kamu
import g4f
from langdetect import detect
from googletrans import Translator

API_URL = "https://sugoi-api.vercel.app/search"
translator = Translator()

def ensure_indonesian(text):
    """Mendeteksi dan menerjemahkan teks ke bahasa Indonesia."""
    try:
        lang = detect(text)
        if lang != 'id':  # Jika bukan bahasa Indonesia, terjemahkan
            return translator.translate(text, dest='id').text
    except Exception as e:
        print(f"Error detecting or translating text: {e}")
    return text

@app.on_message(filters.command(["ajar"], prefixes=["f", "F"]))
async def chat_arvis(client, message):
    """Fungsi percakapan dengan respons dalam <blockquote>."""
    try:
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)
        name = message.from_user.first_name

        if len(message.command) < 2:
            await message.reply_text(f"Halo {name}, saya Fajar. Apa yang bisa saya bantu?")
        else:
            query = message.text.split(' ', 1)[1]
            MODEL = "gpt-3.5-turbo"
            response = g4f.ChatCompletion.create(
                model=MODEL,
                messages=[{"role": "user", "content": query}],
                temperature=0.2
            )
            response_text = ensure_indonesian(response)

            # Membungkus respons dalam <blockquote>
            formatted_response = f"<blockquote>{response_text}</blockquote>"
            await message.reply_text(
                formatted_response, parse_mode=ParseMode.HTML  # Menggunakan ParseMode.HTML
            )
    except Exception as e:
        await message.reply_text(f"Terjadi kesalahan: {e}")

@app.on_message(filters.command(["iri"], prefixes=["s", "S"]))
async def chat_annie(client, message):
    """Fungsi percakapan dengan suara menggunakan TTS."""
    try:
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)
        name = message.from_user.first_name
        if len(message.command) < 2:
            await message.reply_text(f"Halo {name}, saya MEMEX. Apa yang bisa saya bantu?")
        else:
            query = message.text.split(' ', 1)[1]
            MODEL = "gpt-3.5-turbo"
            response = g4f.ChatCompletion.create(
                model=MODEL,
                messages=[{"role": "user", "content": query}],
                temperature=0.2
            )
            response_text = ensure_indonesian(response)

            tts = gTTS(response_text, lang='id')  # Mengubah TTS ke bahasa Indonesia
            tts.save('response.mp3')
            await client.send_voice(chat_id=message.chat.id, voice='response.mp3')

            try:
                os.remove('response.mp3')
            except Exception as e:
                print(f"Error removing file: {e}")
    except Exception as e:
        await message.reply_text(f"Terjadi kesalahan: {e}")


@app.on_message(filters.command(["chatgpt", "ai", "ask"], prefixes=["+", ".", "/", "-", "?", "$", "#", "&"]))
async def chat_gpt(client, message):
    """Fungsi untuk menjalankan percakapan menggunakan GPT."""
    try:
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)

        if len(message.command) < 2:
            await message.reply_text("Halo, saya Fajar. Apa yang bisa saya bantu?")
        else:
            query = message.text.split(' ', 1)[1]
            MODEL = "gpt-3.5-turbo"
            response = g4f.ChatCompletion.create(
                model=MODEL,
                messages=[{"role": "user", "content": query}],
                temperature=0.2
            )
            response_text = ensure_indonesian(response)
            await message.reply_text(response_text)
    except Exception as e:
        await message.reply_text(f"Terjadi kesalahan: {e}")


@app.on_message(filters.command(["bing"], prefixes=["+", ".", "/", "-", "?", "$", "#", "&"]))
async def bing_search(client, message):
    """Fungsi pencarian dengan hasil dibungkus <blockquote>."""
    try:
        if len(message.command) == 1:
            await message.reply_text("Mohon berikan kata kunci untuk pencarian.")
            return

        keyword = " ".join(message.command[1:])
        params = {"keyword": keyword}
        response = requests.get(API_URL, params=params)

        if response.status_code == 200:
            results = response.json()
            if not results:
                await message.reply_text("Tidak ada hasil ditemukan.")
            else:
                message_text = ""
                for result in results[:7]:
                    title = result.get("title", "")
                    link = result.get("link", "")
                    message_text += f"<blockquote><b>{title}</b>\n<a href='{link}'>{link}</a></blockquote>\n\n"

                await message.reply_text(
                    message_text.strip(), parse_mode=ParseMode.HTML, disable_web_page_preview=True
                )
        else:
            await message.reply_text("Maaf, terjadi kesalahan saat pencarian.")
    except Exception as e:
        await message.reply_text(f"Terjadi kesalahan: {str(e)}")
