

# requirements.txt
# >>> https://github.com/KurimuzonAkuma/pyrogram/archive/dev.zip 
# >>> tgcrypto


from pyrogram import Client, filters, types


app = Client(
 name="NandhaBot",
 api_id=12345,
 api_hash="abcd",
 bot_token="bottoken"
      
)

chat_id: int = -1002168230403
to_chat_id: int = -1002201203404


@app.on_message(filters.chat(chat_id))
async def forward(bot: app, message: types.Message):
      await message.forward(
              to_chat_id
      )

app.run()
