

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


async def generate_image(query: str):
    payload = {
        "messages": [{"content": query, "role": "user"}],
        "user_id": str(uuid.uuid4()),
        "codeModelMode": True,
        "agentMode": {
            "mode": True,
            "id": "ImageGenerationLV45LJp",
            "name": "Image Generation"
        },
    }

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Linux; Android 11; Infinix X6816C) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.98 Mobile Safari/537.36"
    }

    api_url = "https://www.blackbox.ai/api/chat"

    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, json=payload, headers=headers) as response:
            response_text = await response.text()
            link = re.search(r"(https://storage\.googleapis\.com/[^\)]+)", response_text)
            return link.group() if link else None

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









     

