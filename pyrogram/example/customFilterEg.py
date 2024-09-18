
from pyrogram import filters, Client

#Let's create a filter that only return True when the user first has '#nandha' hashtag.


hashtag: str = '#nandhabots'

def _hashtag_filter(filter, client, message): return hashtag in message.from_user.first_name

hashtag = filters.create(_hashtag_filter)

# Now you can use them like
@Client.on_message(hashtag) async def _reply(client, message) -> types.Message: return await message.reply_text("Hi my fans 😍")


# Example to making a unique filter

def hashtag(tag: str):
     def _hashtag_filter(filter, client, message):
         return tag in message.from_user.first_name
     return filters.create(_hashtag_filter)


# Now you can use them like
@Client.on_message(hashtag("#dogs")) async def _reply(client, message) -> types.Message: return await message.reply_text("Hi my fans 😍")







