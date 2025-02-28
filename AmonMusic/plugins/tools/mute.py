import asyncio
import logging
from AnonXMusic import app
from AnonXMusic.utils.database import (
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


async def is_admin(client, chat_id, user_id):
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in [STATUS.ADMINISTRATOR, STATUS.OWNER]
    except Exception as e:
        logger.error(f"Error checking admin status: {e}")
        return False


@app.on_message(filters.command("pl") & filters.group & ~(BANNED_USERS))
async def mute_handler(client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not await is_admin(client, chat_id, user_id):
        return await message.reply("Hanya admin atau pemilik grup yang bisa menggunakan perintah ini.")

    if not message.reply_to_message and len(message.command) < 2:
        return await message.reply_text("Berikan saya ID atau nama pengguna yang ingin dimute.")

    user = None
    if message.reply_to_message:
        user = message.reply_to_message.from_user
    else:
        user_input = message.command[1]
        try:
            user = await client.get_users(int(user_input)) if user_input.isdigit() else await client.get_users(user_input)
        except PeerIdInvalid:
            return await message.reply_text("Tidak dapat menemukan pengguna dengan nama tersebut.")
        except Exception as e:
            logging.error(f"Error fetching user: {e}")
            return await message.reply_text(f"Terjadi kesalahan: {e}")

    if user is None:
        return await message.reply_text("Pengguna tidak ditemukan.")

    target_user_id = user.id
    issuer_name = f"{message.from_user.first_name or ''} {message.from_user.last_name or ''}"

    if target_user_id in [user_id, client.me.id]:
        return await message.reply_text("Anda tidak bisa memproses diri sendiri atau bot.")

    if await is_admin(client, chat_id, target_user_id):
        return await message.reply_text("Tidak dapat mute admin grup.")

    muted_users = await get_muted_users_in_group(chat_id)
    if any(u['user_id'] == target_user_id for u in muted_users):
        return await message.reply_text("Pengguna sudah ada di daftar mute.")

    response = await message.reply("`Menambahkan pengguna ke dalam daftar kata terlarang...`")

    try:
        await mute_user_in_group(chat_id, target_user_id, user_id, issuer_name)
    except Exception as e:
        logging.error(f"Error adding user to mute list: {e}")
        return await response.edit("Gagal menambahkan pengguna ke daftar mute.")

    await response.edit(
        f"<b><blockquote>Pengguna berhasil dimute:</blockquote>\n"
        f"- Nama: {user.first_name}\n"
        f"- ID: <code>{target_user_id}</code>\n"
        f"- Oleh: {issuer_name}</b>"
    )

@app.on_message(filters.command("unpl") & filters.group & ~(BANNED_USERS))
async def unmute_handler(client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not await is_admin(client, chat_id, user_id):
        return await message.reply("Hanya admin atau pemilik grup yang bisa menggunakan perintah ini.")

    if not message.reply_to_message and len(message.command) < 2:
        return await message.reply_text("Berikan saya ID atau nama pengguna yang ingin di-unmute.")

    user = None
    if message.reply_to_message:
        user = message.reply_to_message.from_user
    else:
        user_input = message.command[1]
        try:
            user = await client.get_users(int(user_input)) if user_input.isdigit() else await client.get_users(user_input)
        except PeerIdInvalid:
            return await message.reply_text("Tidak dapat menemukan pengguna dengan nama tersebut.")

    if user is None:
        return await message.reply_text("Pengguna tidak ditemukan.")

    target_user_id = user.id
    if target_user_id == user_id:
        return await message.reply_text("Anda tidak bisa memproses diri sendiri.")

    response = await message.reply("`Menghapus pengguna dari daftar mute...`")

    try:
        await unmute_user_in_group(chat_id, target_user_id)
    except Exception as e:
        logging.error(f"Error removing user from mute list: {e}")
        return await response.edit("Gagal menghapus pengguna dari daftar mute.")

    await response.edit(
        f"<blockquote><b>Pengguna berhasil di-unmute:</b>\n"
        f"- Nama: {user.first_name}\n"
        f"- ID: <code>{target_user_id}</code></blockquote>"
    )


@app.on_message(filters.command("listpl") & filters.group & ~(BANNED_USERS))
async def muted(client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not await is_admin(client, chat_id, user_id):
        return await message.reply("Hanya admin atau pemilik grup yang bisa menggunakan perintah ini.")

    muted_users = await get_muted_users_in_group(chat_id)

    if not muted_users:
        return await message.reply("<blockquote>Belum ada pengguna yang di mute</blockquote>")

    response = await message.reply("**Memuat database...**")

    header_msg = "<blockquote><b>Daftar pengguna yang di mute:</b>\n\n</blockquote>"
    msg = header_msg
    num = 0
    max_length = 4096 

    for user in muted_users:
        num += 1
        user_id = user['user_id']
        try:
            user_info = await client.get_users(int(user_id))
            user_name = f"{user_info.first_name or ''} {user_info.last_name or ''}"
        except PeerIdInvalid:
            user_name = "Tidak dikenal"
        muted_by_name = user['muted_by']['name']
        
        user_info_msg = (
            f"<blockquote>â˜ ï¸ <b>{num}. {user_name}</b>\n"
            f"> ID: <code>{user_id}</code>\n"
            f"> Di-mute oleh: {muted_by_name}\n\n</blockquote>"
        )

        if len(msg) + len(user_info_msg) > max_length:
            await message.reply(msg, disable_web_page_preview=True)
            msg = header_msg + user_info_msg
        else:
            msg += user_info_msg

    await message.reply(msg, disable_web_page_preview=True)
    await response.delete()


@app.on_message(filters.command("clearpl") & filters.group & ~(BANNED_USERS))
async def clear_muted(client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not await is_admin(client, chat_id, user_id):
        return await message.reply("Hanya admin atau pemilik grup yang bisa menggunakan perintah ini.")

    muted_users = await get_muted_users_in_group(chat_id)

    if not muted_users:
        return await message.reply("**Tidak ada pengguna yang di mute untuk dihapus.**")

    await clear_muted_users_in_group(chat_id)

    await message.reply("**Semua pengguna yang di mute telah dihapus untuk grup ini.**")


@app.on_message(filters.group, group=-3)
async def delete_muted_messages(client, message: Message):
    if message.from_user is None:
        return

    user_id = message.from_user.id
    chat_id = message.chat.id

    muted_users = await get_muted_users_in_group(chat_id)
    
    if any(u['user_id'] == user_id for u in muted_users):
        try:
            await client.delete_messages(chat_id, message_ids=[message.id])
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await client.delete_messages(chat_id, message_ids=[message.id])
        except Exception as e:
            logging.error(f"Failed to delete muted message: {e}")
