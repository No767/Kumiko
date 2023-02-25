import os
import urllib.parse

import discord
from discord.ext import commands
from dotenv import load_dotenv
from kumiko_servers import KumikoServer

load_dotenv()

POSTGRES_PASSWORD = urllib.parse.quote_plus(os.getenv("Postgres_Password"))
POSTGRES_SERVER_IP = os.getenv("Postgres_Server_IP")
POSTGRES_DATABASE = os.getenv("Postgres_Kumiko_Database")
POSTGRES_USERNAME = os.getenv("Postgres_Username")
POSTGRES_PORT = os.getenv("Postgres_Port")
CONNECTION_URI = f"asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
MODELS = ["kumiko_servers.models"]


class ServerJoinHandlers(commands.Cog):
    """Kumiko's Server Join Handlers"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        serverExists = await KumikoServer.filter(id=guild.id).exists()
        if serverExists is False:
            await KumikoServer.create(id=guild.id, name=guild.name, announcements=False)


def setup(bot):
    bot.add_cog(ServerJoinHandlers(bot))
