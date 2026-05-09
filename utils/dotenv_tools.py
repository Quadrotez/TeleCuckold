import os

from getpass import getpass
from dotenv import load_dotenv, set_key

from config import DOTENV_FILE_PATH

load_dotenv()
def init() -> None:    
    keys = (("API_ID", 1, 1), ("API_HASH", 1, 1), ("PROXY_URL", 0, 0), ("CHATS_TO_HANDLE", 1, 0))

    for key, mandatory, hide in keys:
        if (not mandatory and os.getenv("INITED")) or (mandatory and os.getenv(key) is not None):
            continue
        if not mandatory:
            if not input(f"Желаете ли установить {key}? (Y/n): ").lower() == "y":
                continue
        
        value = getpass(f"Введите {key}: ") if hide else input(f"Введите {key}: ")
        set_key(DOTENV_FILE_PATH, key, value)
    set_key(DOTENV_FILE_PATH, "INITED", "1")
    load_dotenv()
