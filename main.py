import os


from telethon import TelegramClient, events

from utils import dotenv_tools, proxy_tools
from config import SESSION_NAME

dotenv_tools.init()

API_ID, API_HASH = os.environ["API_ID"], os.environ["API_HASH"]

proxy = os.getenv("PROXY_URL")
if proxy:
    proxy = proxy_tools.url_to_dict(proxy)

client = TelegramClient(SESSION_NAME, API_ID, API_HASH, proxy=proxy)

@client.on(events.NewMessage)
async def my_ev_hand(event: events.NewMessage.Event):
    await event.reply(event.message.message)

client.start()
client.run_until_disconnected()