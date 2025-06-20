import import asyncio
from AmonMusic import app
from config import OWNER_ID, LOG_GROUP_ID
from pyrogram import filters
from AmonMusic.misc import SUDOERS

BOT_ID = 7791093481
BAN_PROCESS = {}

def extract_chat_id(arg):
    if arg.startswith("https://t.me/"):
        return arg.split("/")[-1]
    elif arg.startswith("@"):
        return arg
    elif arg.startswith("-100") and arg[1:].isdigit():
        return int(arg)
    elif arg.isdigit():
        return int(arg)
    return None

@app.on_message(filters.command("banall") & SUDOERS)
async def ban_all(_, msg):
    args = msg.text.split()
    target = msg.chat.id
    mode = "slow"

    for arg in args[1:]:
        if arg.lower() in ["fast", "slow"]:
            mode = arg.lower()
        else:
            resolved = extract_chat_id(arg)
            if resolved:
                try:
                    chat = await app.get_chat(resolved)
                    target = chat.id
                except Exception as e:
                    return await msg.reply_text(f"❌**Gagal mengambil grup target:**\n<code>{e}</code>")

    banned, skipped = 0, 0

    if BAN_PROCESS.get(target):
        return await msg.reply_text("⚠️ **Proses ban all sudah berjalan di grup ini.**\n**Gunakan** `/stopbanall` **untuk menghentikannya.**")

    try:
        bot_member = await app.get_chat_member(target, BOT_ID)
        if not bot_member.privileges or not bot_member.privileges.can_restrict_members:
            return await msg.reply_text("❌ **Bot tidak punya izin ban di grup ini.**")
    except Exception as e:
        return await msg.reply_text(f"❌ **Gagal cek status bot:**\n<code>{e}</code>")

    BAN_PROCESS[target] = True
    await msg.reply_text(f"🔨 **Mulai banall semua member di** <code>{target}</code> **dengan mode** <b>{mode.upper()}</b>...\n**Ketik** /stopbanall **untuk menghentikan.**")

    try:
        async for member in app.get_chat_members(target):
            if not BAN_PROCESS.get(target):
                await msg.reply_text("🛑 **Proses dihentikan secara manual.**")
                break

            user = member.user

            if (
                member.status in ("administrator", "owner")
                or user.is_bot
                or user.id in (BOT_ID, msg.from_user.id)
            ):
                skipped += 1
                continue

            try:
                await app.ban_chat_member(target, user.id)
                banned += 1

                if banned % 10 == 0:
                    print(f"[INFO] Dibanned: {banned} | Dilewati: {skipped}")

                if mode == "slow":
                    await asyncio.sleep(0.3)
                elif mode == "fast" and banned % 25 == 0:
                    await asyncio.sleep(1)

            except Exception as e:
                skipped += 1
                print(f"[ERROR] Gagal ban {user.id}: {e}")
                continue

    except Exception as e:
        await msg.reply_text(f"❌ G**agal loop member:**\n<code>{e}</code>")

    finally:
        BAN_PROCESS.pop(target, None)

    report = (
        f"✅ <b>Memex Banall Selesai</b>\n"
        f"👥 <b>Grup:</b> <code>{target}</code>\n"
        f"🔨 <b>Dibanned:</b> <code>{banned}</code>\n"
        f"⏭️ <b>Dilewati:</b> <code>{skipped}</code>\n"
        f"⚙️ <b>Mode:</b> <code>{mode}</code>\n"
        f"👑 <b>Oleh:</b> {msg.from_user.mention} (`{msg.from_user.id}`)"
    )

    await msg.reply_text(f"✅ P**roses selesai.**\n🔨 **Dibanned:** `{banned}`\n⏭️ **Dilewati:** `{skipped}`")
    await app.send_message(LOG_GROUP_ID, report)


@app.on_message(filters.command("stopbanall") & SUDOERS)
async def stop_ban_all(_, msg):
    args = msg.text.split(maxsplit=1)
    target = msg.chat.id

    if len(args) > 1:
        resolved = extract_chat_id(args[1].strip())
        if resolved:
            try:
                chat = await app.get_chat(resolved)
                target = chat.id
            except:
                pass

    if BAN_PROCESS.get(target):
        BAN_PROCESS[target] = False
        await msg.reply_text("🛑 **Proses ban dihentikan.**")

await app.send_message(
            LOG_GROUP_ID,
            f"🛑 <b>Memex Ban Dihentikan</b>\n"
            f"👥 <b>Grup:</b> <code>{target}</code>\n"
            f"👑 <b>Oleh:</b> {msg.from_user.mention} (`{msg.from_user.id}`)"
        )
    else:
        await msg.reply_text("ℹ️ **Tidak ada proses ban yang sedang berjalan.**")
