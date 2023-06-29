import os
from pathlib import Path

from dotenv import load_dotenv
from Libs.cache import KumikoCPManager

path = Path(__file__).parents[2].joinpath(".env")

load_dotenv(dotenv_path=path)

REDIS_URI = os.environ["REDIS_URI"]

kumikoCP: KumikoCPManager = KumikoCPManager(uri=REDIS_URI)
