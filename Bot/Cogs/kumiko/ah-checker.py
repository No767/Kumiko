import asyncio
import logging
import os
from datetime import datetime

from dateutil import parser
from discord.ext import commands
from economy_utils import KumikoAuctionHouseUtils
from rin_exceptions import ItemNotFound

POSTGRES_PASSWORD = os.getenv("Postgres_Password")
POSTGRES_SERVER_IP = os.getenv("Postgres_Server_IP")
POSTGRES_PORT = os.getenv("Postgres_Port")
POSTGRES_AH_DATABASE = os.getenv("Postgres_Kumiko_Database")
POSTGRES_USERNAME = os.getenv("Postgres_Username")
AH_CONNECTION_URI = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:{POSTGRES_PORT}/{POSTGRES_AH_DATABASE}"

ahUtils = KumikoAuctionHouseUtils()

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] | %(asctime)s [AH Checker] >> %(message)s",
    datefmt="[%m/%d/%Y] [%I:%M:%S %p %Z]",
)


class InitAHItemPurger:
    def __init__(self):
        self.self = self

    async def mainProc(self):
        """The main proc of the AH Item Checker"""
        logging.info("Successfully started AH Item Checker")
        while True:
            await asyncio.sleep(86400)
            mainRes = await ahUtils.obtainAHItemPassed(
                passed=False, uri=AH_CONNECTION_URI
            )
            try:
                if len(mainRes) == 0:
                    raise ItemNotFound
                else:
                    for item in mainRes:
                        mainItem = dict(item)
                        today = datetime.now()
                        parsedDate = parser.isoparse(dict(mainItem)["date_added"])
                        if parsedDate < today:
                            await ahUtils.setAHItemBoolean(
                                uuid=dict(mainItem)["uuid"],
                                passed=True,
                                uri=AH_CONNECTION_URI,
                            )
                        elif parsedDate == today:
                            await ahUtils.setAHItemBoolean(
                                uuid=dict(mainItem)["uuid"],
                                passed=True,
                                uri=AH_CONNECTION_URI,
                            )
                        elif parsedDate > today:
                            continue
            except ItemNotFound:
                logging.warn(
                    "No items found in the AH database. Continuing to check for more"
                )
                continue


class AHItemChecker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_connect(ctx):
        initProc = InitAHItemPurger()
        task = asyncio.create_task(initProc.mainProc(), name="AHItemChecker")
        background_tasks = set()
        background_tasks.add(await task)
        task.add_done_callback(background_tasks.discard)


def setup(bot):
    bot.add_cog(AHItemChecker(bot))
