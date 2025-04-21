from dotenv import load_dotenv
import os, json

load_dotenv(dotenv_path="secrets/.env")

def get_config_values(labels:list):
    values = []
    with open("config/config.json", "r") as f:
        config = json.load(f)
        for label in labels:
            value = config.get(label, None)
            values.append(value)
    return values

def set_chat_id(new_id:int):
    with open("config/config.json", "r+") as f:
        config = json.load(f)
        config["chat_id"] = new_id
        f.seek(0)
        json.dump(config, f, indent=2)
        f.truncate()

def get_chat_id():
    with open("config/config.json", "r") as f:
        config = json.load(f)
        return config["chat_id"]


BOT_TOKEN = os.environ.get("BOT_TOKEN")
POLL_INTERVAL, QUERIES_PATH, GMAIL_CREDS_PATH, GMAIL_TOKEN_PATH = get_config_values(["poll_interval",
                                                                                     "query_path",
                                                                                     "gmail_creds_path",
                                                                                     "gmail_token_path"])