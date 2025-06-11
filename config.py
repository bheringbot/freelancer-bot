import os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
RESPONDER_EM_GRUPO = os.getenv("RESPONDER_EM_GRUPO", "False") == "True"
