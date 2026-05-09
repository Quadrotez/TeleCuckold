import os

from getpass import getpass
from dotenv import load_dotenv, set_key

from config import DOTENV_FILE_PATH

_ = load_dotenv()


def init() -> None:
    keys = (
        {"key": "API_ID", "mandatory": True, "hide_input": True},
        {"key": "API_HASH", "mandatory": True, "hide_input": True},
        {"key": "PROXY_URL", "mandatory": False, "hide_input": False},
        {"key": "CHATS_TO_HANDLE", "mandatory": True, "hide_input": False},
        {"key": "SAVE_MEDIA", "mandatory": False, "hide_input": False, "description": "Сохранять ли медиафайлы в избранное? (Y/n)"},
    )

    for key in keys:
        if (not key["mandatory"] and os.getenv("INITED") is not None) or (
            key["mandatory"] and os.getenv(key["key"]) is not None  # pyright: ignore[reportArgumentType]
        ):
            continue
        if not key["mandatory"]:
            if not input(f"Желаете ли установить {key["key"]}? (Y/n): ").lower() == "y":
                continue
        if key.get("description"):
            print(key["description"])
        value = getpass(f"Введите {key["key"]}: ") if key["hide_input"] else input(f"Введите {key["key"]}: ")
        _ = set_key(DOTENV_FILE_PATH, key["key"], value)  # pyright: ignore[reportArgumentType]
    _ = set_key(DOTENV_FILE_PATH, "INITED", "1")
    _ = load_dotenv()
