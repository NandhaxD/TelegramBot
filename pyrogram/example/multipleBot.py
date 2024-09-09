from pyrogram import Client, filters
import pyrogram
import logging
import asyncio

logging.basicConfig(level=logging.INFO)


API_ID = 123456789
API_HASH = "abcde"
TOKEN_01 = "123456789:abcd"
TOKEN_02 = "123456789:abcd"


# Custom handler decorator
def handlers(bot: Client, handler_type, filters):
    def decorator(func):
        bot.add_handler(handler_type(func, filters))  # Use the function as part of the handler
        return func
    return decorator


bot1 = Client(
    name='name_01', 
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=TOKEN_01
)


bot2 = Client(
     name='name_02', 
     api_id=API_ID,
     api_hash=API_HASH,
     bot_token=TOKEN_02
)


@handlers(bot1, pyrogram.handlers.MessageHandler, filters.command('start'))
@handlers(bot2, pyrogram.handlers.MessageHandler, filters.command('start'))
async def start(client: pyrogram.Client, message: pyrogram.types.Message):
    m = message
    bot = await client.get_me()
    user = m.from_user
    await m.reply_text(
         f"Hello, {user.first_name}! I'm {bot.first_name} 🙋 What do you want?"
    )


async def main() -> None:
     apps = [bot1, bot2]
     await pyrogram.compose(apps)
     
  
if __name__ == "__main__":
       loop = asyncio.get_event_loop()
       loop.run_until_complete(main())
  
