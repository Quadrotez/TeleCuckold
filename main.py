import os
import logging

from telethon import TelegramClient, events

from utils import dotenv_tools, proxy_tools
from config import SESSION_NAME

dotenv_tools.init()

API_ID, API_HASH = os.environ["API_ID"], os.environ["API_HASH"]

proxy = os.getenv("PROXY_URL")
if proxy:
    proxy = proxy_tools.url_to_dict(proxy)

client = TelegramClient(SESSION_NAME, API_ID, API_HASH, proxy=proxy)

chats_to_handle = ("me")

@client.on(events.NewMessage(chats=chats_to_handle))
async def h_global_message(event: events.NewMessage.Event):
    await event.reply(event.message.message)

logging.basicConfig(level=logging.INFO)

client.start()
logging.log(msg="Клиент запущен", level=logging.INFO)
client.run_until_disconnected()