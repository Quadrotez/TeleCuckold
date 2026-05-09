import os

from getpass import getpass
from dotenv import load_dotenv, set_key

from config import DOTENV_FILE_PATH

load_dotenv()
def init() -> None:
    if not os.path.exists(DOTENV_FILE_PATH):
        keys = (("API_ID", 1), ("API_HASH", 1), ("PROXY_URL", 0))
        for key, mandatory in keys:
            if not mandatory:
                if not input(f"Желаете ли установить {key}? (Y/n): ").lower() == "y":
                    continue
            
            value = getpass(f"Введите {key}: ")
            set_key(DOTENV_FILE_PATH, key, value)