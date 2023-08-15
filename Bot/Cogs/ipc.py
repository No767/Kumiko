import os
from typing import Dict

from discord.ext import commands, ipc
from discord.ext.ipc.objects import ClientPayload
from discord.ext.ipc.server import Server
from dotenv import load_dotenv
from kumikocore import KumikoCore

load_dotenv()

IPC_SECRET_KEY = os.getenv("IPC_SECRET_KEY")
IPC_HOST = os.environ["IPC_HOST"]


class IPCServer(commands.Cog):
    def __init__(self, bot: KumikoCore):
        self.bot = bot
        self.ipc = ipc.Server(  # type: ignore
            self.bot, secret_key=IPC_SECRET_KEY, host=IPC_HOST
        )

    async def cog_load(self) -> None:
        await self.ipc.start()

    async def cog_unload(self) -> None:
        await self.ipc.stop()

    @Server.route()
    async def health_check(self, data: ClientPayload) -> Dict:
        bot_status = self.bot.is_closed()
        status = "down" if bot_status is True else "ok"
        return {"status": status}


async def setup(bot: KumikoCore):
    await bot.add_cog(IPCServer(bot))
