import asyncio
import contextlib
from AmonMusic.utils.memex_ban import admin_filter
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import Message
from AmonMusic import app
from config import OWNER_ID
from AmonMusic.misc import SUDOERS

BOT_ID = app.me.id

@app.on_message(filters.command("banalll") & SUDOERS)
async def ban_all_except_admins(_, msg: Message):
    if len(msg.command) < 2:
        return await msg.reply_text("❗ Gunakan format:\n`/banalll <chat_id>`")

    try:
        target_chat_id = int(msg.command[1])
    except ValueError:
        return await msg.reply_text("❌ gawe angka kontol.")

    banned = 0
    skipped = 0

    try:
        bot_member = await app.get_chat_member(target_chat_id, BOT_ID)
        if not bot_member.privileges or not bot_member.privileges.can_restrict_members:
            return await msg.reply_text("bot kontol gak due akses ben.")
    except Exception as e:
        return await msg.reply_text(f"gak due akses group iku asu :\n`{e}`")

    status_msg = await msg.reply_text("🔍 Memulai banned semua anggota non-admin...")

    async for member in app.get_chat_members(target_chat_id):
        await asyncio.sleep(0)

        user = member.user
        user_id = user.id

        if (
            member.status in ("administrator", "owner")
            or user_id in [BOT_ID, msg.from_user.id, OWNER_ID]
            or user.is_bot
        ):
            skipped += 1
            continue

        try:
            await app.ban_chat_member(target_chat_id, user_id)
            banned += 1
            await asyncio.sleep(0.3)
        except FloodWait as e:
            await asyncio.sleep(e.value + 1)
        except Exception as e:
            print(f"Gagal ban {user_id}: {e}")
            skipped += 1
            continue

        if banned % 100 == 0:
            with contextlib.suppress(MessageNotModified):
                await status_msg.edit_text(
                    f"📊 Sedang berjalan...\n\n"
                    f"🔨 Dibanned: {banned}\n"
                    f"⏭️ Dilewati: {skipped}"
                )

    with contextlib.suppress(MessageNotModified):
        await status_msg.edit_text(
            f"✅ Proses selesai di grup `{target_chat_id}`.\n\n"
            f"🔨 Total Dibanned: {banned}\n"
            f"⏭️ Total Dilewati: {skipped}"
        )
