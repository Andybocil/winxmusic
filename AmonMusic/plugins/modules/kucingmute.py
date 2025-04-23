import asyncio
import logging
from AmonMusic import app
from AmonMusic.utils.database import (
    mute_user_in_group,
    unmute_user_in_group,
    get_muted_users_in_group,
    clear_muted_users_in_group,
)
from pyrogram import filters
from pyrogram.errors import FloodWait, PeerIdInvalid
from pyrogram.enums import ChatMemberStatus as STATUS
from pyrogram.types import Message
from config import BANNED_USERS

logger = logging.getLogger(__name__)


async def is_admin(client, chat_id, user_id):
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in [STATUS.ADMINISTRATOR, STATUS.OWNER]
    except Exception as e:
        logger.error(f"Error checking admin status: {e}")
        return False


@app.on_message(filters.command("pl") & filters.group & ~BANNED_USERS)
async def mute_handler(client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not await is_admin(client, chat_id, user_id):
        return await message.reply("❌ Hanya admin atau pemilik grup yang bisa menggunakan perintah ini.")

    if not message.reply_to_message and len(message.command) < 2:
        return await message.reply_text("⚠ Berikan saya ID atau nama pengguna yang ingin dimute.")

    user = message.reply_to_message.from_user if message.reply_to_message else None

    if not user:
        user_input = message.command[1]
        try:
            user = await client.get_users(int(user_input)) if user_input.isdigit() else await client.get_users(user_input)
        except PeerIdInvalid:
            return await message.reply_text("❌ Tidak dapat menemukan pengguna dengan nama tersebut.")
        except Exception as e:
            logger.error(f"Error fetching user: {e}")
            return await message.reply_text(f"⚠ Terjadi kesalahan: {e}")

    if not user:
        return await message.reply_text("❌ Pengguna tidak ditemukan.")

    target_user_id = user.id
    issuer_name = f"{message.from_user.first_name or ''} {message.from_user.last_name or ''}".strip()

    if target_user_id in [user_id, client.me.id]:
        return await message.reply_text("⚠ Anda tidak bisa memproses diri sendiri atau bot.")

    if await is_admin(client, chat_id, target_user_id):
        return await message.reply_text("❌ Tidak dapat mute admin grup.")

    muted_users = await get_muted_users_in_group(chat_id)
    if any(u["user_id"] == target_user_id for u in muted_users):
        return await message.reply_text("✅ Pengguna sudah ada di daftar mute.")

    response = await message.reply("🔄 Menambahkan pengguna ke dalam daftar mute...")

    try:
        await mute_user_in_group(chat_id, target_user_id, user_id, issuer_name)
    except Exception as e:
        logger.error(f"Error adding user to mute list: {e}")
        return await response.edit("❌ Gagal menambahkan pengguna ke daftar mute.")

    await response.edit(
        f"<b>🔇 Pengguna berhasil dimute:</b>\n"
        f"👤 Nama: {user.first_name}\n"
        f"🆔 ID: <code>{target_user_id}</code>\n"
        f"🔹 Oleh: {issuer_name}"
    )


@app.on_message(filters.command("unpl") & filters.group & ~BANNED_USERS)
async def unmute_handler(client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not await is_admin(client, chat_id, user_id):
        return await message.reply("❌ Hanya admin atau pemilik grup yang bisa menggunakan perintah ini.")

    if not message.reply_to_message and len(message.command) < 2:
        return await message.reply_text("⚠ Berikan saya ID atau nama pengguna yang ingin di-unmute.")

    user = message.reply_to_message.from_user if message.reply_to_message else None

    if not user:
        user_input = message.command[1]
        try:
            user = await client.get_users(int(user_input)) if user_input.isdigit() else await client.get_users(user_input)
        except PeerIdInvalid:
            return await message.reply_text("❌ Tidak dapat menemukan pengguna dengan nama tersebut.")

    if not user:
        return await message.reply_text("❌ Pengguna tidak ditemukan.")

    target_user_id = user.id

    response = await message.reply("🔄 Menghapus pengguna dari daftar mute...")

    try:
        await unmute_user_in_group(chat_id, target_user_id)
    except Exception as e:
        logger.error(f"Error removing user from mute list: {e}")
        return await response.edit("❌ Gagal menghapus pengguna dari daftar mute.")

    await response.edit(
        f"✅ <b>Pengguna berhasil di-unmute:</b>\n"
        f"👤 Nama: {user.first_name}\n"
        f"🆔 ID: <code>{target_user_id}</code>"
    )


@app.on_message(filters.command("listpl") & filters.group & ~BANNED_USERS)
async def muted(client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not await is_admin(client, chat_id, user_id):
        return await message.reply("❌ Hanya admin atau pemilik grup yang bisa menggunakan perintah ini.")

    muted_users = await get_muted_users_in_group(chat_id)

    if not muted_users:
        return await message.reply("📜 <b>Belum ada pengguna yang dimute.</b>")

    msg = "<b>📋 Daftar pengguna yang dimute:</b>\n\n"
    for num, user in enumerate(muted_users, start=1):
        msg += f"🔇 {num}. <code>{user['user_id']}</code> (🔹 Oleh: {user['muted_by']['name']})\n"

    await message.reply(msg, disable_web_page_preview=True)


@app.on_message(filters.command("clearpl") & filters.group & ~BANNED_USERS)
async def clear_muted(client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not await is_admin(client, chat_id, user_id):
        return await message.reply("❌ Hanya admin atau pemilik grup yang bisa menggunakan perintah ini.")

    muted_users = await get_muted_users_in_group(chat_id)

    if not muted_users:
        return await message.reply("✅ Tidak ada pengguna yang dimute untuk dihapus.")

    await clear_muted_users_in_group(chat_id)

    await message.reply("✅ Semua pengguna yang dimute telah dihapus.")


@app.on_message(filters.group, group=-3)
async def delete_muted_messages(client, message: Message):
    if not message.from_user:
        return

    chat_id = message.chat.id
    user_id = message.from_user.id

    muted_users = await get_muted_users_in_group(chat_id)

    if any(u["user_id"] == user_id for u in muted_users):
        try:
            await client.delete_messages(chat_id, [message.id])
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await client.delete_messages(chat_id, [message.id])
        except Exception as e:
            logger.error(f"❌ Gagal menghapus pesan pengguna yang dimute: {e}")
