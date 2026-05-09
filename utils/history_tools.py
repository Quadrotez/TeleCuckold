import os
import json

from datetime import datetime

from config import HISTORY_PATH


os.makedirs(HISTORY_PATH, exist_ok=True)

history_file = os.path.join(
    HISTORY_PATH,
    f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
)

history = []


def add_message(who: str, what: str):
    if not what.strip():
        return

    history.append({
        "who": who,
        "what": what
    })

    with open(history_file, "w", encoding="utf-8") as file:
        json.dump(
            history,
            file,
            ensure_ascii=False,
            indent=4
        )