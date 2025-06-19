import asyncio
from pyrogram import filters, enums
from AmonMusic import app
from config import OWNER_ID
from AmonMusic.misc import SUDOERS

BOT_ID = app.me.id 

@app.on_message(filters.command("banalll") & filters.group & SUDOERS)
async def ban_all(_, msg):
    chat_id = msg.chat.id
    banned = 0
    skipped = 0

    try:
        bot_member = await app.get_chat_member(chat_id, BOT_ID)
        if not bot_member.privileges or not bot_member.privileges.can_restrict_members:
            return await msg.reply_text("❌ Bot tidak memiliki izin untuk membanned anggota di grup ini.")
    except Exception as e:
        return await msg.reply_text(f"⚠️ Gagal mengambil status bot: {e}")

    async for member in app.get_chat_members(chat_id):
        user_id = member.user.id

        if (
            user_id in [BOT_ID, msg.from_user.id]
            or user_id in SUDOERS
            or (
                member.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]
                and member.privileges
                and member.privileges.can_restrict_members
            )
        ):
            skipped += 1
            continue

        try:
            await app.ban_chat_member(chat_id, user_id)
            banned += 1
            await asyncio.sleep(0.2)
        except Exception as e:
            print(f"Gagal ban {user_id}: {e}")
            skipped += 1

    await msg.reply_text(
        f"✅ Proses selesai.\n\n"
        f"🔨 Dibanned: {banned} user\n"
        f"⏭️ Dilewati: {skipped} user"
    )
