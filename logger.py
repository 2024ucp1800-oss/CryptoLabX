from datetime import datetime

LOG_FILE = "outputs/execution.log"

def log_action(action):
    current_time = datetime.now()

    with open(LOG_FILE, "a") as file:
        file.write(
            f"{current_time.strftime('%Y-%m-%d %H:%M:%S')} - {action}\n"
        )
