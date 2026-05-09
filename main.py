import os
import asyncio
import logging

from telethon import TelegramClient, events

from utils import dotenv_tools, proxy_tools, data_tools
from config import FIRST_SESSION_NAME, SECOND_SESSION_NAME

dotenv_tools.init()

API_ID, API_HASH = os.environ["API_ID"], os.environ["API_HASH"]

proxy = os.getenv("PROXY_URL")
if proxy:
    proxy = proxy_tools.url_to_dict(proxy)

client1 = TelegramClient(FIRST_SESSION_NAME, API_ID, API_HASH, proxy=proxy)
client2 = TelegramClient(SECOND_SESSION_NAME, API_ID, API_HASH, proxy=proxy)

chats_to_handle = os.environ["CHATS_TO_HANDLE"].split()

@client1.on(events.NewMessage(chats=chats_to_handle))
async def h_global_message(event: events.NewMessage.Event):
    chat_id = (await event.get_chat()).id
    client1_id = (await client1.get_me()).id

    if chat_id == client1_id:
        chat_id = "me" 

    if data_tools.check_ignore(event.message.message):
        return 
    answer = data_tools.check_answer(event.message.message)
    if answer[0]:
        if answer[1]:
            await event.reply(answer[1])
        if answer[2]:
            await client2.send_message(chat_id, answer[2])
        return

    await client2.send_message(chat_id, event.message.message)

@client2.on(events.NewMessage(chats=chats_to_handle))
async def h_global_message(event: events.NewMessage.Event):
    chat_id = (await event.get_chat()).id
    client2_id = (await client2.get_me()).id

    if chat_id == client2_id:
        chat_id = "me" 

    if data_tools.check_ignore(event.message.message):
        return 
    answer = data_tools.check_answer(event.message.message)
    print(answer)
    if answer[0]:
        if answer[1]:
            await event.reply(answer[1])
        if answer[2]:
            await client1.send_message(chat_id, answer[2])
        return
    await client1.send_message(chat_id, event.message.message)

async def main():
    global client1_id, client2_id

    await client1.start()
    await client2.start()

    for chat in chats_to_handle:
        await client1.send_message(chat, "/next")
        await client2.send_message(chat, "/next")

    logging.basicConfig(level=logging.INFO)

    logging.log(msg="Клиенты запущены   ", level=logging.INFO)
    await asyncio.gather(
        client1.run_until_disconnected(),
        client2.run_until_disconnected()
    )

if __name__ == "__main__":
    asyncio.run(main())