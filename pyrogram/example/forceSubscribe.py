
from pyrogram import Client, filters, errors, types

import logging


logging.basicConfig(level=logging.INFO)

app = Client(name="Nandha", api_id=13257951, api_hash="d8ea642aedb736d40035bc05f0cfd477", bot_token="6990642754:AAGORkNCef_9Gsibtb9HGSj3KHEXlx8MwNA")


FCHAT_ID: int = -1001995603469


@app.on_message(filters.command('help'))
async def help(bot: app, m: types.Message):
     await m.reply_text('help msg here')

@app.on_message(group=-1)
async def start(bot: app, m: types.Message):
      user_id = m.from_user.id
      mention = m.from_user.mention
  
      try:
      	 user = await bot.get_chat_member(FCHAT_ID, user_id)
      except errors.UserNotParticipant:       
      	  chat = await bot.get_chat(FCHAT_ID)
      	  await m.reply_text(f"hello! {mention} Please join the chat and then start the bot: {chat.title}")
      	  await m.stop_propagation()


app.run()
