import asyncio
import logging
from datetime import datetime

from dateutil import parser
from discord.ext import commands
from economy_utils import KumikoAuctionHouseUtils
from rin_exceptions import ItemNotFound

ahUtils = KumikoAuctionHouseUtils()

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] | %(asctime)s >> %(message)s",
    datefmt="[%m/%d/%Y] [%I:%M:%S %p %Z]",
)


class InitAHItemPurger:
    def __init__(self):
        self.self = self

    async def mainProc(self):
        """The main proc of the AH Item Checker"""
        logging.info("Successfully started Kumiko's AH Item Checker")
        while True:
            await asyncio.sleep(86400)
            mainRes = await ahUtils.obtainAHItemPassed(False)
            try:
                if len(mainRes) == 0:
                    raise ItemNotFound
                else:
                    for item in mainRes:
                        mainItem = dict(item)
                        today = datetime.now()
                        parsedDate = parser.isoparse(dict(mainItem)["date_added"])
                        if parsedDate < today:
                            await ahUtils.setAHItemBoolean(dict(mainItem)["uuid"], True)
                        elif parsedDate == today:
                            await ahUtils.setAHItemBoolean(dict(mainItem)["uuid"], True)
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
