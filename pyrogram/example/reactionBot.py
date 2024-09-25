

import asyncio
import logging

from pyrogram import Client, compose, filters

logging.basicConfig(level=logging.INFO)



targetChatIds = [-100123456789, ...] 



TOKENS = [
    "....",
    "...." # add your bot tokens here...
]

API_ID = 12345678
API_HASH = "abcde..."

clients = [Client(name=f"ReactBot{index}", api_id=API_ID, api_hash=API_HASH, bot_token=token) for index, token in enumerate(TOKENS)]
   
# remember to add bot admin in the targeted channels.
           
                  
for app in clients:
	   @app.on_message()
	   async def _reacts(app, message):
	   	      if message.chat.id in targetChatIds:
	   	            await message.react("❤️")




async def main():
       await compose(clients)

    
loop = asyncio.get_event_loop()
loop.run_until_complete(main())   
