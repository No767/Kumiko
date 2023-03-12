import asyncio
import os
from typing import Dict

from discord.ext import commands, ipc
from discord.ext.ipc.objects import ClientPayload
from discord.ext.ipc.server import Server
from dotenv import load_dotenv

load_dotenv()

IPC_SECRET_KEY = os.getenv("IPC_SECRET_KEY")


class IPCServer(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.ipc = ipc.Server(self.bot, secret_key=IPC_SECRET_KEY)
        self.bot.loop.create_task(self.bot.ipc.start())

    def cog_unload(self) -> None:
        asyncio.run(self.bot.ipc.stop())

    @Server.route()
    async def get_user_data(self, data: ClientPayload) -> Dict:
        user = self.get_user(data.user_id)
        return user._to_minimal_user_json()


def setup(bot):
    bot.add_cog(IPCServer(bot))
