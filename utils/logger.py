import os
from datetime import datetime

LOG_FILE = os.path.join("outputs", "execution.log")


def log_action(action):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    current_time = datetime.now()
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(f"{current_time.strftime('%Y-%m-%d %H:%M:%S')} - {action}\n")
