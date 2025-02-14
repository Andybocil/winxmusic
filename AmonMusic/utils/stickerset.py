from typing import List

from pyrogram import Client, errors, raw

async def get_sticker_set_by_name(
    client: Client, name: str
) -> raw.base.messages.StickerSet:
    try:
        result = await client.invoke(
            raw.functions.messages.GetStickerSet(
                stickerset=raw.types.InputStickerSetShortName(short_name=name),
                hash=0,
            )
        )
        return result
    except errors.BadRequest as e:
        if "STICKERSET_INVALID" in str(e):
            return None
        raise  # Reraise exception if it's not related to StickerSetInvalid
    except Exception as e:
        print(f"An error occurred in get_sticker_set_by_name: {e}")
        return None


async def create_sticker_set(
    client: Client,
    owner: int,
    title: str,
    short_name: str,
    stickers: List[raw.base.InputStickerSetItem],
) -> raw.base.messages.StickerSet:
    try:
        result = await client.invoke(
            raw.functions.stickers.CreateStickerSet(
                user_id=await client.resolve_peer(owner),
                title=title,
                short_name=short_name,
                stickers=stickers,
            )
        )
        return result
    except Exception as e:
        print(f"An error occurred in create_sticker_set: {e}")
        return None


async def add_sticker_to_set(
    client: Client,
    stickerset: raw.base.messages.StickerSet,
    sticker: raw.base.InputStickerSetItem,
) -> raw.base.messages.StickerSet:
    try:
        return await client.invoke(
            raw.functions.stickers.AddStickerToSet(
                stickerset=raw.types.InputStickerSetShortName(
                    short_name=stickerset.set.short_name
                ),
                sticker=sticker,
            )
        )
    except errors.exceptions.bad_request_400.StickerEmojiInvalid:
        print("Error: Invalid emoji for the sticker.")
        return None
    except errors.exceptions.bad_request_400.StickersetInvalid:
        print(f"Error: Stickerset '{stickerset.set.short_name}' is invalid.")
        return None
    except Exception as e:
        print(f"Unexpected error occurred while adding a sticker: {e}")
        return None


async def create_sticker(
    sticker: raw.base.InputDocument, emoji: str
) -> raw.base.InputStickerSetItem:
    try:
        return raw.types.InputStickerSetItem(document=sticker, emoji=emoji)
    except Exception as e:
        print(f"Unexpected error occurred while creating the sticker: {e}")
        return None
