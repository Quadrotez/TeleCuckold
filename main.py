import os
import asyncio
import logging

from telethon import TelegramClient, events
from io import BytesIO

from utils import dotenv_tools, proxy_tools, data_tools, history_tools
from config import FIRST_SESSION_NAME, SECOND_SESSION_NAME

dotenv_tools.init()

API_ID, API_HASH = os.environ["API_ID"], os.environ["API_HASH"]

proxy = os.getenv("PROXY_URL")
if proxy:
    proxy = proxy_tools.url_to_dict(proxy)

client1 = TelegramClient(FIRST_SESSION_NAME, API_ID, API_HASH, proxy=proxy)
client2 = TelegramClient(SECOND_SESSION_NAME, API_ID, API_HASH, proxy=proxy)

chats_to_handle = os.environ["CHATS_TO_HANDLE"].split()



async def handle_message(event, source_client, target_client, source_me_id):
    chat_id = (
        "me"
        if event.chat_id == source_me_id
        else event.chat_id
    )

    message = event.message
    text = event.raw_text or ""

    history_tools.add_message(
        FIRST_SESSION_NAME
        if source_client == client1
        else SECOND_SESSION_NAME,
        text
    )

    if message.media:

        if text.strip():
            answer = data_tools.check_answer(text)

            if answer[0]:
                if answer[1]:
                    await source_client.send_message(chat_id, answer[1])

                if answer[2]:
                    await target_client.send_message(chat_id, answer[2])

                return

            if data_tools.check_ignore(text):
                return

        file_bytes = await source_client.download_media(
            message,
            file=bytes
        )

        if event.photo:
            photo_file = BytesIO(file_bytes)
            photo_file.name = "photo.jpg"

            await target_client.send_file(
                chat_id,
                photo_file,
                caption=text if text.strip() else None
            )

            return

        attrs = (
            message.media.document.attributes
            if getattr(message.media, "document", None)
            else []
        )

        upload_file = BytesIO(file_bytes)

        upload_file.name = (
            message.file.name
            or (
                "voice.ogg"
                if event.voice
                else "video_note.mp4"
                if event.video_note
                else "sticker.webp"
                if event.sticker
                else "file"
            )
        )

        kwargs = {}

        if event.voice:
            kwargs["voice_note"] = True

        if event.video_note:
            kwargs["video_note"] = True

        await target_client.send_file(
            chat_id,
            upload_file,
            caption=text if text.strip() else None,
            attributes=attrs,
            mime_type=message.file.mime_type,
            force_document=event.document and not (
                event.video
                or event.audio
                or event.voice
                or event.video_note
                or event.sticker
            ),
            **kwargs
        )

        return

    answer = data_tools.check_answer(text)

    if answer[0]:
        if answer[1]:
            await source_client.send_message(chat_id, answer[1])

        if answer[2]:
            await target_client.send_message(chat_id, answer[2])

        return

    if data_tools.check_ignore(text):
        return

    await target_client.send_message(chat_id, text)

@client1.on(events.NewMessage(chats=chats_to_handle))
async def handler1(event):
    await handle_message(event, client1, client2, client1_me_id)


@client2.on(events.NewMessage(chats=chats_to_handle))
async def handler2(event):
    await handle_message(event, client2, client1, client2_me_id)

client1_me_id = None
client2_me_id = None

async def main():
    global client1_me_id, client2_me_id

    await client1.start()
    await client2.start()

    client1_me_id = (await client1.get_me()).id
    client2_me_id = (await client2.get_me()).id

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