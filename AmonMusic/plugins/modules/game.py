from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client, enums, filters
#from config import *
import asyncio
from AmonMusic import app as app

from pyrogram.handlers import MessageHandler


@app.on_message(filters.command("dice"))
async def dice(bot, message):
    x=await bot.send_dice(message.chat.id)
    m=x.dice.value
    await message.reply_text(f"Hey {message.from_user.mention} your Score is : {m}",quote=True)
  
@app.on_message(filters.command("dart"))
async def dart(bot, message):
    x=await bot.send_dice(message.chat.id, "🎯")
    m=x.dice.value
    await message.reply_text(f"Hey {message.from_user.mention} your Score is : {m}",quote=True)

@app.on_message(filters.command("basket"))
async def basket(bot, message):
    x=await bot.send_dice(message.chat.id, "🏀")
    m=x.dice.value
    await message.reply_text(f"Hey {message.from_user.mention} your Score is : {m}",quote=True)
@app.on_message(filters.command("jackpot"))
async def basket(bot, message):
    x=await bot.send_dice(message.chat.id, "🎰")
    m=x.dice.value
    await message.reply_text(f"Hey {message.from_user.mention} your Score is : {m}",quote=True)
@app.on_message(filters.command("ball"))
async def basket(bot, message):
    x=await bot.send_dice(message.chat.id, "🎳")
    m=x.dice.value
    await message.reply_text(f"Hey {message.from_user.mention} your Score is : {m}",quote=True)
@app.on_message(filters.command("football"))
async def basket(bot, message):
    x=await bot.send_dice(message.chat.id, "⚽")
    m=x.dice.value
    await message.reply_text(f"Hey {message.from_user.mention} your Score is : {m}",quote=True)

@app.on_message(filters.command("catur"))
async def catur(bot, message):
    try:
        # Buat inline keyboard dengan tombol menuju game catur
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Main Catur 🏁", url="https://t.me/GameFactoryBot?start=catur")]
            ]
        )

        # Kirim pesan dengan keyboard
        await bot.send_message(
            chat_id=message.chat.id,
            text="Mari main catur! Klik tombol di bawah untuk memulai:",
            reply_markup=keyboard
        )
    except Exception as error:
        await message.reply_text(f"Terjadi kesalahan: {error}", quote=True)
