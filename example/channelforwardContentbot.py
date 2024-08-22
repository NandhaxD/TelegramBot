

# requirements.txt
# >>> https://github.com/KurimuzonAkuma/pyrogram/archive/dev.zip 
# >>> tgcrypto



import logging

logging.basicConfig(level=logging.INFO)

from pyrogram import Client, filters


app = Client(
name="Nandhabot",
api_id=12345,
api_hash="api_hash",
bot_token="7508215693:AAEorpF2EkWbc7BmzX7rIkNh81Yo7HUIq1k"
)


channel_id = -1002168230403
to_channel_id= -1002201203404


@app.on_message(filters.chat(channel_id))
async def forwarder(bot, message):
      m = message
      await m.forward(to_channel_id)
      
      

app.run()
