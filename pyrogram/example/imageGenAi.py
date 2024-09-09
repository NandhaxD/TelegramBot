

import aiohttp
import logging
import re
import uuid
import asyncio

logging.basicConfig(level=logging.INFO)
from pyrogram import Client, filters, types, idle



api_id = 12345678
api_hash = "....."
token = "....."
name = "ImageGenBot"

nandha = Client(
   name=name, 
   api_id=api_id,
   api_hash=api_hash,
   bot_token=token
)



@nandha.on_message(filters.text & filters.private)
async def ImageGenCmd(bot, message) -> types.Message:
     prompt = message.text
     msg = await message.reply_text("✨ **Imagining....**")
     try:
        photo_url = await generate_image(prompt)
        await msg.reply_photo(photo_url)
     except Exception as e:
         return await msg.edit_text(f"❌ Error report to @NandhaSupport: {repr(e)}")
     return await msg.delete()



async def main():
     await nandha.start()
     await idle()
     

if __name__ == "__main__":
  loop = asyncio.get_event_loop()
  loop.run_until_complete(main())









     

