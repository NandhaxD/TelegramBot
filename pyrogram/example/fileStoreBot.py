import os
import logging
import asyncio

logging.basicConfig(level=logging.INFO)

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Configs
API_HASH = 
APP_ID = 
BOT_TOKEN = 
TRACK_CHANNEL = -1002178137218
OWNER_ID = 5696053228 # change to 'all' for everyone can store file in the bot.

#Button
START_BUTTONS=[
    [
        InlineKeyboardButton('✨ Developer', url="https://t.me/nandha"),
        InlineKeyboardButton('🌀 Dev Channel', url='https://t.me/nandhabots'),
    ],
]

# Running bot
nandhaBot = Client('Nandha-File-Sharing', api_id=APP_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Notify about bot start
with nandhaBot:
    info = nandhaBot.get_me()
    nandhaBot_username = info.username  # Better call it global once due to telegram flood id
    logging.info(
    "####################################################################################################\n\n"
    "✅ Bot Started!\n"
    f"Bot Name: {info.first_name}\n"
    f"Bot Telegram ID: {info.id}"
    "\n\n####################################################################################################"
    )
    nandhaBot.send_message(
                    chat_id=int(OWNER_ID), 
                    text="Bot started!"
    )


# Start & Get file
@nandhaBot.on_message(filters.command('start') & filters.private)
async def _startfile(bot, update):
    if update.text == '/start':
        await update.reply_text(
            f"I'm File-Sharing!\nYou can share any telegram files and get the sharing link using this bot!\n\n/help for more details...",
            True, reply_markup=InlineKeyboardMarkup(START_BUTTONS))
        return

    if len(update.command) != 2:
        return
    code = update.command[1]
    if '-' in code:
        msg_id = code.split('-')[-1]
        unique_id = '-'.join(code.split('-')[0:-1])

        if not msg_id.isdigit():
            return
        try:  
            check_media_group = await bot.get_media_group(TRACK_CHANNEL, int(msg_id))
            check = check_media_group[0]  
        except Exception:
            check = await bot.get_messages(TRACK_CHANNEL, int(msg_id))

        if check.empty:
            await update.reply_text('Error: [Message does not exist]\n/help for more details...')
            return
        if check.video:
            unique_idx = check.video.file_unique_id
        elif check.photo:
            unique_idx = check.photo.file_unique_id
        elif check.audio:
            unique_idx = check.audio.file_unique_id
        elif check.document:
            unique_idx = check.document.file_unique_id
        elif check.sticker:
            unique_idx = check.sticker.file_unique_id
        elif check.animation:
            unique_idx = check.animation.file_unique_id
        elif check.voice:
            unique_idx = check.voice.file_unique_id
        elif check.video_note:
            unique_idx = check.video_note.file_unique_id
        if unique_id != unique_idx.lower():
            return
        try:  
            await bot.copy_media_group(update.from_user.id, TRACK_CHANNEL, int(msg_id))
        except Exception:
            await check.copy(update.from_user.id)
    else:
        return


# Help msg
@nandhaBot.on_message(filters.command('help') & filters.private)
async def _help(bot, update):
    await update.reply_text("Supported file types:\n\n- Video\n- Audio\n- Photo\n- Document\n- Sticker\n- GIF\n- Voice note\n- Video note\n\n If bot didn't respond, contact @nandha", True)


async def __reply(update, copied):
    msg_id = copied.id
    if copied.video:
        unique_idx = copied.video.file_unique_id
    elif copied.photo:
        unique_idx = copied.photo.file_unique_id
    elif copied.audio:
        unique_idx = copied.audio.file_unique_id
    elif copied.document:
        unique_idx = copied.document.file_unique_id
    elif copied.sticker:
        unique_idx = copied.sticker.file_unique_id
    elif copied.animation:
        unique_idx = copied.animation.file_unique_id
    elif copied.voice:
        unique_idx = copied.voice.file_unique_id
    elif copied.video_note:
        unique_idx = copied.video_note.file_unique_id
    else:
        await copied.delete()
        return

    await update.reply_text(
        'Here is Your Sharing Link:',
        True,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('Sharing Link',
                                  url=f'https://t.me/{nandhaBot_username}?start={unique_idx.lower()}-{str(msg_id)}')]
        ])
    )
    await asyncio.sleep(0.5)  # Wait do to avoid 5 sec flood ban 

# Store media_group
media_group_id = 0
@nandhaBot.on_message(filters.media & filters.private & filters.media_group)
async def _main_grop(bot, update):
    global media_group_id
    if OWNER_ID == 'all':
        pass
    elif int(OWNER_ID) == update.from_user.id:
        pass
    else:
        return

    if int(media_group_id) != int(update.media_group_id):
        media_group_id = update.media_group_id
        copied = (await bot.copy_media_group(TRACK_CHANNEL, update.from_user.id, update.id))[0]
        await __reply(update, copied)

    else:
        return


# Store file
@nandhaBot.on_message(filters.media & filters.private & ~filters.media_group)
async def _main(bot, update):
    if OWNER_ID == 'all':
        pass
    elif int(OWNER_ID) == update.from_user.id:
        pass
    else:
        return

    copied = await update.copy(TRACK_CHANNEL)
    await __reply(update, copied)


nandhaBot.run()
