import os

from discord.ext import commands, ipcx
from dotenv import load_dotenv
from kumikocore import KumikoCore

load_dotenv()

IPC_SECRET_KEY = os.getenv("IPC_SECRET_KEY")
IPC_HOST = os.environ["IPC_HOST"]


class IPCRoutes(commands.Cog):
    def __init__(self, bot: KumikoCore):
        self.bot = bot

    @ipcx.route()
    async def healthcheck(self, data):
        bot_status = self.bot.is_closed()
        if bot_status is True:
            return False
        return True


async def setup(bot: KumikoCore):
    await bot.add_cog(IPCRoutes(bot))
