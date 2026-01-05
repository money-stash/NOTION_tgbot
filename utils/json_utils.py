import json

from utils.logger import logger


async def get_lanuage_msg(language_code: str, message_key: str) -> str:
    with open("database/languages.json", "r", encoding="utf-8") as file:
        languages = json.load(file)

    key = f"{message_key}_{language_code}"

    logger.info(
        f"Fetching language message({message_key}_{language_code}) for key: {key}"
    )
    return languages.get(key, "Message not found")
