import os
import uuid
from datetime import datetime

import discord
from dateutil import parser
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands
from dotenv import load_dotenv
from economy_utils import KumikoQuestsUtils
from rin_exceptions import ItemNotFound

load_dotenv()

POSTGRES_PASSWORD = os.getenv("Postgres_Password_Dev")
POSTGRES_SERVER_IP = os.getenv("Postgres_Server_IP_Dev")
POSTGRES_QUESTS_DATABASE = os.getenv("Postgres_Quests_Database")
POSTGRES_USERNAME = os.getenv("Postgres_Username_Dev")
CONNECTION_URI = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_QUESTS_DATABASE}"

questsUtil = KumikoQuestsUtils()


class ServerQuests(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    quests = SlashCommandGroup(
        "quests",
        "Commands for the quests feature in Kumiko",
        guild_ids=[970159505390325842],
    )
    questsAccount = quests.create_subgroup(
        "account", "mostly for the server account", guild_ids=[970159505390325842]
    )

    @questsAccount.command(name="init")
    async def questsInit(
        self,
        ctx,
        *,
        name: Option(str, "The name of the server account"),
        description: Option(str, "The description for the server account"),
        amount: Option(int, "The amount to first start off with"),
    ):
        """Initialize the server's quests account"""
        # TODO: Add a check to make sure that the user is the owner of the server
        checkForDupeRes = await questsUtil.getServerAcct(ctx.guild.id, CONNECTION_URI)
        if len(checkForDupeRes) == 0:
            guildID = ctx.guild.id
            serverAcctUUID = str(uuid.uuid4())
            creationDate = datetime.now().isoformat()
            await questsUtil.insServerAcct(
                guild_id=guildID,
                uuid=serverAcctUUID,
                date_created=creationDate,
                name=name,
                description=description,
                balance=amount,
                uri=CONNECTION_URI,
            )
            await ctx.respond(f"Created {ctx.guild.name}'s server quests account!")
        else:
            await ctx.respond("You can't create more server accounts...")

    @questsAccount.command(name="view")
    async def questsAcctView(self, ctx):
        """View the server's quests account"""
        mainRes = await questsUtil.getServerAcct(ctx.guild.id, CONNECTION_URI)
        try:
            if len(mainRes) == 0:
                raise ItemNotFound
            else:
                for item in mainRes:
                    mainItem = dict(item)
                    embed = discord.Embed()
                    embed.title = mainItem["name"]
                    embed.description = mainItem["description"]
                    embed.add_field(name="Guild", value=ctx.guild.name, inline=True)
                    embed.add_field(
                        name="Creation Date",
                        value=parser.isoparse(mainItem["date_created"]).strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        inline=True,
                    )
                    embed.add_field(
                        name="Current Balance", value=mainItem["balance"], inline=True
                    )
                    embed.set_thumbnail(url=ctx.guild.icon.url)
                    await ctx.respond(embed=embed)
        except ItemNotFound:
            embedError = discord.Embed()
            embedError.description = (
                "It seems like your server doesn't have an account yet..."
            )
            await ctx.respond(embed=embedError)


def setup(bot):
    bot.add_cog(ServerQuests(bot))
