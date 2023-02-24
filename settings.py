import os
import sys
import urllib.parse
from pathlib import Path

from dotenv import load_dotenv

path = Path(__file__).parent
envPath = os.path.join(str(path), "Bot", ".env")
sys.path.append(os.path.join(str(path), "Bot"))
sys.path.append(os.path.join(str(path), "Bot", "Libs"))

load_dotenv(dotenv_path=envPath)

POSTGRES_PASSWORD = urllib.parse.quote_plus(os.getenv("Postgres_Password"))
POSTGRES_SERVER_IP = os.getenv("Postgres_Server_IP")
POSTGRES_DATABASE = os.getenv("Postgres_Kumiko_Database")
POSTGRES_USERNAME = os.getenv("Postgres_Username")
POSTGRES_PORT = os.getenv("Postgres_Port")
CONNECTION_URI = f"asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
MODELS = [
    "kumiko_genshin_wish_sim.models",
    "kumiko_servers.models",
    "kumiko_admin_logs.models",
    "kumiko_economy.models",
    "aerich.models",
]

TORTOISE_ORM = {
    "connections": {
        "default": CONNECTION_URI,
    },
    "apps": {
        "models": {"models": MODELS, "default_connection": "default"},
    },
}
