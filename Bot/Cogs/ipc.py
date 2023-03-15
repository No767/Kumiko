import os
from typing import Dict

from discord.ext import commands, ipc
from discord.ext.ipc.objects import ClientPayload
from discord.ext.ipc.server import Server
from dotenv import load_dotenv

load_dotenv()

IPC_SECRET_KEY = os.getenv("IPC_SECRET_KEY")
IPC_HOST = os.environ["IPC_HOST"]


class IPCServer(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ipc = ipc.Server(  # type: ignore
            self.bot, secret_key=IPC_SECRET_KEY, host=IPC_HOST
        )

    async def cog_load(self) -> None:
        await self.ipc.start()

    async def cog_unload(self) -> None:
        await self.ipc.stop()

    @Server.route()
    async def get_user_data(self, data: ClientPayload) -> Dict:
        user = self.bot.get_user(data.user_id)
        return user._to_minimal_user_json()  # type: ignore


async def setup(bot: commands.Bot):
    await bot.add_cog(IPCServer(bot))
