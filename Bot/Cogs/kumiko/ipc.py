import asyncio
import logging
import os
from typing import Dict

from discord.ext import commands, ipc
from discord.ext.ipc.objects import ClientPayload
from discord.ext.ipc.server import Server
from dotenv import load_dotenv

load_dotenv()

IPC_SECRET_KEY = os.getenv("IPC_Secret_Key")


class IPCServer(commands.Cog):
    """Kumiko's IPC Server"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        if not hasattr(bot, "ipc"):
            bot.ipc = ipc.Server(self.bot, secret_key=IPC_SECRET_KEY)
        asyncio.run(self.bot.ipc.start())

    def cog_unload(self):
        asyncio.run(self.bot.ipc.stop())
        self.bot.ipc = None

    @Server.route()
    async def get_user_data(self, data: ClientPayload) -> Dict:
        user = self.get_user(data.user_id)
        return user._to_minimal_user_json()

    @Server.route()
    async def create_embed(self, data: ClientPayload) -> None:
        print(data.embed_content)
        logging.debug(f"Embed created, and sent to {data.channel_id}")


def setup(bot):
    bot.add_cog(IPCServer(bot))
