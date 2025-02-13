import asyncio
from AmonMusic import app
from pyrogram import Client, filters
from datetime import datetime, timedelta
from pyrogram.errors import FloodWait
from AmonMusic.core.mongo import db as amon
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from AmonMusic.utils.database import get_served_users, get_served_chats


OWNER_ID = 7369463399
