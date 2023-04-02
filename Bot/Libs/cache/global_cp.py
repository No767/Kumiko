import os
from pathlib import Path

from dotenv import load_dotenv
from Libs.cache import KumikoCPManager

path = Path(__file__).parents[2].joinpath(".env")

load_dotenv(dotenv_path=path)

REDIS_HOST = os.environ["REDIS_HOST"]
REDIS_PORT = os.environ["REDIS_PORT"]
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

kumikoCP: KumikoCPManager = KumikoCPManager(
    host=REDIS_HOST, port=int(REDIS_PORT), password=REDIS_PASSWORD
)
