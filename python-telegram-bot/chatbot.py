# requirements.txt
# >> python-telegram-bot

"""
This bot code was developed by https://t.me/nandhabots, 
a channel dedicated to helping new bot developers to learn how to create bot on telegram
today practice a Customized chatbots using Python.

By: @Nandha
"""

import asyncio
import contextlib
import logging
import httpx
import re
import ast
import uuid
import json
from typing import NoReturn
from telegram import Bot, Update, constants
from telegram.error import Forbidden, NetworkError


# Logging setup for application-wide debugging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


TOKEN = "123456789:abcd" # Replace with your bot token from @BotFather
char_id = "Vegeta9z9K0T7" # AGENT-ID from https://blackbox.ai
char_name = "Vegeta" # CHARACTER-NAME as same as you entered name for create Agent [Optional]

async def BlackBoxChat(user_id: str, messages: list) -> dict:
    """
    Function to send user input to the BlackBox AI API and return AI-generated responses.
    
    Args:
        user_id (str): A unique identifier for the user interacting with the bot.
        messages (list): A list of dictionaries containing user prompts and messages.

    Returns:
        dict: A dictionary containing the AI-generated reply text.
    """
    data = {
        "messages": messages,
        "user_id": user_id,
        "codeModelMode": True,
        "agentMode": {
            "mode": True,
            "id": char_id,
            "name": char_name
        },
        "trendingAgentMode": {}
    }
    headers = {"Content-Type": "application/json"}
    url = "https://www.blackbox.ai/api/chat"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data)
            response_text = response.text

            # Clean the response and extract relevant data if available
            cleaned_response_text = re.sub(r'^\$@\$(.*)\$@\$', '', response_text)
            aiText = cleaned_response_text.strip()

            # Parse any data links if included in the response
            if "$~~~$" in aiText:
                data_links_match = re.search(r'\$~~~\$(.*?)\$~~~\$', aiText, flags=re.DOTALL)
                if data_links_match:
                    data_links = data_links_match.group(1)
                    if ast.literal_eval(data_links):
                        text = "\n"
                        for data in json.loads(data_links):
                            if (title := data.get('title')) and (link := data.get('link')):
                                text += f"• [{title}]({link})\n\n"
                        index = aiText.rfind("$~~~$")
                        text += aiText[index + 5:]
                        aiText = text

            return {'reply': aiText}

    except Exception as e:
        logger.error(f"Error in BlackBoxChat: {str(e)}")
        return {'reply': f'❌ Something went wrong: {str(e)}'}


async def main() -> NoReturn:
    """
    The main function that continuously fetches updates from Telegram, processes incoming
    messages, and interacts with the bot.
    """
   
    async with Bot(TOKEN) as bot:
        last_update_id = 0

        logging.info("BOT STARTED TO LISTENING...")
        while True:
            try:
                # Fetch updates from the bot
                updates = await bot.get_updates(offset=last_update_id + 1)

                if updates:
                    for update in updates:
                        # Process new updates
                        if update.update_id != last_update_id:
                            last_update_id = update.update_id
                            if getattr(update.message, 'text', False):
                                await chatbot(bot, update)

                await asyncio.sleep(2.5)  # Control polling rate

            except (Forbidden, NetworkError) as e:
                logger.error(f"Error occurred: {e}")
                await asyncio.sleep(5)  # Retry delay on error


async def chatbot(bot: Bot, update: Update):
    """
    Handles the processing of incoming messages and sends the response back to the user.
    
    Args:
        bot (Bot): The Telegram bot instance.
        update (Update): The Telegram update containing the user's message.
    """
    # Send a temporary reply before processing the full response
    msg = await update.message.reply_text("⚡", quote=True)
    prompt = update.message.text
    user = update.message.from_user
    user_id = str(uuid.uuid4())
    messages = [{"role": "user", "content": prompt}]
    
    # Get response from BlackBox AI
    reply_text = (await BlackBoxChat(user_id, messages))['reply']
    
    try:
        await msg.edit_text(reply_text, parse_mode=constants.ParseMode.MARKDOWN)
        logger.info(f'👥 User {user.full_name} ({user.id}) asked: "{prompt}" at {update.message.date}')
    
    except Exception as e:
        logger.error(f"Error occurred for prompt '{prompt}': {e}")


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):  # Gracefully handle Ctrl-C exit
        asyncio.run(main())
