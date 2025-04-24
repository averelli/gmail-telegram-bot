import json
import logging
from config import QUERIES_PATH

logger = logging.getLogger("email-telegram-bot")

def load_queries() -> list:
    try:
        with open(QUERIES_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.info("Queries file does not exist, creating empty.")
        with open(QUERIES_PATH, "w") as f:
            json.dump([], f)
            return []
    except Exception as e:
        logger.error(f"Error while loading queries: {e}", exc_info=True)
        raise
    

def save_queries(queries:list):
    try:
        with open(QUERIES_PATH, "w") as f:
            json.dump(queries, f, indent=2)
    except Exception as e:
        logger.error(f"Error while saving queries: {e}", exc_info=True)
        raise


def update_processed_messages(q_id:int, msg_id:str):
    """Adds a message id to processed_messages list for provided query id"""
    logger.info(f"[]")
    old_queries = load_queries()
    new_queries = []

    for q in old_queries:
        if q["id"] == q_id:
            q["processed_messages"].append(msg_id)
            new_queries.append(q)
        else:
            new_queries.append(q)

    save_queries(new_queries)