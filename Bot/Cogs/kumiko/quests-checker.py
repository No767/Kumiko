import asyncio
import logging
import os
from datetime import datetime

import uvloop
from dateutil import parser
from discord.ext import commands
from dotenv import load_dotenv
from economy_utils import KumikoQuestsUtils
from rin_exceptions import NoItemsError

load_dotenv()

POSTGRES_PASSWORD = os.getenv("Postgres_Password")
POSTGRES_SERVER_IP = os.getenv("Postgres_Server_IP")
POSTGRES_QUESTS_DATABASE = os.getenv("Postgres_Kumiko_Database")
POSTGRES_PORT = os.getenv("Postgres_Port")
POSTGRES_USERNAME = os.getenv("Postgres_Username")
CONNECTION_URI = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:{POSTGRES_PORT}/{POSTGRES_QUESTS_DATABASE}"

questUtils = KumikoQuestsUtils()

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] | %(asctime)s [Quests Checker] >> %(message)s",
    datefmt="[%m/%d/%Y] [%I:%M:%S %p %Z]",
)


async def mainQuestsProc() -> None:
    """The main process of the Quests Checker"""
    logging.info("Successfully started Quests Checker")
    while True:
        await asyncio.sleep(3600)
        activeQuests = await questUtils.getAllActiveQuests(
            active=True, uri=CONNECTION_URI
        )
        try:
            if len(activeQuests) == 0:
                raise NoItemsError
            else:
                for questItem in activeQuests:
                    today = datetime.now()
                    parsedDate = parser.isoparse(dict(questItem)["end_datetime"])
                    if parsedDate < today:
                        await questUtils.setQuestActiveStatus(
                            uuid=dict(questItem)["uuid"],
                            active=False,
                            uri=CONNECTION_URI,
                        )
                    elif parsedDate == today:
                        await questUtils.setQuestActiveStatus(
                            uuid=dict(questItem)["uuid"],
                            active=False,
                            uri=CONNECTION_URI,
                        )
                    elif parsedDate > today:
                        continue
        except NoItemsError:
            logging.warn(
                "No quests found to be active in the DB. Continuing to check for more"
            )
            continue


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class QuestsChecker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_connect(ctx):
        task = asyncio.create_task(mainQuestsProc(), name="QuestsChecker")
        backgroundTasks = set()
        backgroundTasks.add(await task)
        task.add_done_callback(backgroundTasks.discard)


def setup(bot):
    bot.add_cog(QuestsChecker(bot))
