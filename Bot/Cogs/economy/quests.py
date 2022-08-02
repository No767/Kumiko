import asyncio
import os
import uuid
from datetime import datetime

import discord
import uvloop
from dateutil import parser
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands, pages
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


class DeleteAllView(discord.ui.View):
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True

    @discord.ui.button(
        label="Yes",
        row=0,
        style=discord.ButtonStyle.primary,
        emoji=discord.PartialEmoji.from_str("<:check:314349398811475968>"),
    )
    async def button_callback(self, button, interaction):
        itemUUIDAuth = await questsUtil.getItemUUIDAuth(
            guild_id=interaction.guild_id,
            user_id=interaction.user.id,
            uri=CONNECTION_URI,
        )
        try:
            if len(itemUUIDAuth) == 0:
                raise ItemNotFound
            else:
                for item in itemUUIDAuth:
                    await questsUtil.purgeUserQuests(
                        guild_id=interaction.guild.id,
                        user_id=interaction.user.id,
                        uuid=item,
                        uri=CONNECTION_URI,
                    )
                await interaction.response.send_message(
                    "All quests belonging to you have been purged.", ephemeral=True
                )
        except ItemNotFound:
            await interaction.response.send_message(
                "You don't have any quests to delete!", ephemeral=True
            )

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @discord.ui.button(
        label="No",
        row=0,
        style=discord.ButtonStyle.primary,
        emoji=discord.PartialEmoji.from_str("<:xmark:314349398824058880>"),
    )
    async def second_button_callback(self, button, interaction):
        await interaction.response.send_message(
            "Well glad you choose not to...", ephemeral=True
        )

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


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
    questsDelete = quests.create_subgroup(
        "delete", "deletes quests", guild_ids=[970159505390325842]
    )
    questsView = quests.create_subgroup(
        "view", "views the quests", guild_ids=[970159505390325842]
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
                uuid=serverAcctUUID,
                guild_id=guildID,
                date_created=creationDate,
                name=name,
                description=description,
                balance=amount,
                uri=CONNECTION_URI,
            )
            await ctx.respond(f"Created {ctx.guild.name}'s server quests account!")
        else:
            await ctx.respond("You can't create more server accounts...")

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

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

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @questsAccount.command(name="restock")
    async def setQuestsAccountBalance(
        self, ctx, *, new_amount: Option(int, "The new amount of petals to restock to")
    ):
        """Updates the amount of petals on the server account"""
        checkBal = await questsUtil.getServerAcct(
            guild_id=ctx.guild.id, uri=CONNECTION_URI
        )
        try:
            if len(checkBal) == 0:
                raise ItemNotFound
            else:
                for items in checkBal:
                    mainItems = dict(items)
                    if int(new_amount) < int(10000):
                        totalBal = int(mainItems["balance"]) + int(new_amount)
                        await questsUtil.updateServerBal(
                            guild_id=mainItems["guild_id"],
                            uuid=mainItems["uuid"],
                            balance_amount=totalBal,
                            uri=CONNECTION_URI,
                        )
                        await ctx.respond(
                            f"Successfully updated {ctx.guild.name}'s server account balance to {totalBal} petals!"
                        )
                    else:
                        await ctx.respond(
                            "Sadly you can't update the account due to the limits on there... Please try again with a smaller amount."
                        )
        except ItemNotFound:
            await ctx.respond(
                "It seems like your server doesn't have an account yet..."
            )

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @quests.command(name="create")
    async def createQuests(
        self,
        ctx,
        *,
        name: Option(str, "The name of the quest"),
        description: Option(str, "The description of the quest"),
        reward: Option(int, "The amount of petals to reward for completion"),
        end_date: Option(str, "The end date for the quest"),
        end_time: Option(str, "The end time for this quest"),
    ):
        """Creates a quest"""
        questUUIDItem = str(uuid.uuid4())
        guildID = ctx.guild.id
        dateCreated = datetime.now().isoformat()
        endDateFormatted = parser.parse(f"{end_date} {end_time}").isoformat()
        await questsUtil.createQuests(
            uuid=questUUIDItem,
            guild_id=guildID,
            creator=ctx.author.id,
            date_created=dateCreated,
            end_datetime=endDateFormatted,
            name=name,
            description=description,
            reward=reward,
            active=True,
            uri=CONNECTION_URI,
        )
        await ctx.respond(f"Created quest: {name}")

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @questsView.command(name="active")
    async def viewQuest(self, ctx):
        """Views all of the quests active as of now"""
        activeQuests = await questsUtil.getActiveQuests(
            guild_id=ctx.guild.id, active=True, uri=CONNECTION_URI
        )
        try:
            if len(activeQuests) == 0:
                raise ItemNotFound
            else:
                mainPages = pages.Paginator(
                    pages=[
                        discord.Embed(
                            title=dict(items)["name"],
                            description=dict(items)["description"],
                        )
                        .add_field(
                            name="Reward", value=dict(items)["reward"], inline=True
                        )
                        .add_field(
                            name="End Date",
                            value=parser.isoparse(dict(items)["end_datetime"]).strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ),
                            inline=True,
                        )
                        .add_field(
                            name="Creator",
                            value=f'{await self.bot.get_or_fetch_user(dict(items)["creator"])}',
                            inline=True,
                        )
                        .add_field(
                            name="Date Created",
                            value=parser.isoparse(dict(items)["date_created"]).strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ),
                            inline=True,
                        )
                        for items in activeQuests
                    ],
                    loop_pages=True,
                )
                await mainPages.respond(ctx.interaction, ephemeral=False)
        except ItemNotFound:
            embedError = discord.Embed()
            embedError.description = "It seems like there are no active quests on the server yet... Please try again"
            await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @questsView.command(name="inactive")
    async def getInactiveQuests(self, ctx):
        """Gets all of the inactive quests"""
        inactiveQuests = await questsUtil.getActiveQuests(
            guild_id=ctx.guild.id, active=False, uri=CONNECTION_URI
        )
        try:
            if len(inactiveQuests) == 0:
                raise ItemNotFound
            else:
                mainPages = pages.Paginator(
                    pages=[
                        discord.Embed(
                            title=dict(items)["name"],
                            description=dict(items)["description"],
                        )
                        .add_field(
                            name="Reward", value=dict(items)["reward"], inline=True
                        )
                        .add_field(
                            name="End Date",
                            value=parser.isoparse(dict(items)["end_datetime"]).strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ),
                            inline=True,
                        )
                        .add_field(
                            name="Creator",
                            value=f'{await self.bot.get_or_fetch_user(dict(items)["creator"])}',
                            inline=True,
                        )
                        .add_field(
                            name="Date Created",
                            value=parser.isoparse(dict(items)["date_created"]).strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ),
                            inline=True,
                        )
                        for items in inactiveQuests
                    ],
                    loop_pages=True,
                )
                await mainPages.respond(ctx.interaction, ephemeral=False)
        except ItemNotFound:
            embedError = discord.Embed()
            embedError.description = "It seems like there are no inactive quests on the server yet... Please try again"
            await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @questsView.command(name="all")
    async def getAllQuests(self, ctx):
        """ "Gets all of the quests, both active and inactive ones"""
        allQuests = await questsUtil.getAllQuests(
            guild_id=ctx.guild.id, uri=CONNECTION_URI
        )
        try:
            if len(allQuests) == 0:
                raise ItemNotFound
            else:
                mainPages = pages.Paginator(
                    pages=[
                        discord.Embed(
                            title=dict(items)["name"],
                            description=dict(items)["description"],
                        )
                        .add_field(
                            name="Reward", value=dict(items)["reward"], inline=True
                        )
                        .add_field(
                            name="End Date",
                            value=parser.isoparse(dict(items)["end_datetime"]).strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ),
                            inline=True,
                        )
                        .add_field(
                            name="Creator",
                            value=f'{await self.bot.get_or_fetch_user(dict(items)["creator"])}',
                            inline=True,
                        )
                        .add_field(
                            name="Date Created",
                            value=parser.isoparse(dict(items)["date_created"]).strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ),
                            inline=True,
                        )
                        .add_field(
                            name="Active?", value=dict(items)["active"], inline=True
                        )
                        for items in allQuests
                    ],
                    loop_pages=True,
                )
                await mainPages.respond(ctx.interaction, ephemeral=False)
        except ItemNotFound:
            embedError = discord.Embed()
            embedError.description = (
                "It seems like there are no quests on the server. Please try again"
            )
            await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @quests.command(name="update")
    async def updateQuests(
        self,
        ctx,
        *,
        name: Option(str, "The name of the quest"),
        reward: Option(int, "The new reward to update to"),
        end_date: Option(str, "The new date to update to"),
        end_time: Option(str, "The new time to update to"),
    ):
        """Updates the quest with new info"""
        mainQuest = await questsUtil.getQuestViaName(
            guild_id=ctx.guild.id, name=name, uri=CONNECTION_URI
        )
        try:
            if len(mainQuest) == 0:
                raise ItemNotFound
            else:
                fullDateTime = parser.parse(f"{end_date} {end_time}").isoformat()
                for items in mainQuest:
                    await questsUtil.updateQuest(
                        guild_id=ctx.guild.id,
                        uuid=dict(items)["uuid"],
                        reward=reward,
                        new_end_datetime=fullDateTime,
                        uri=CONNECTION_URI,
                    )
                    await ctx.respond(f"Updated {name} with an reward of {reward}")
        except ItemNotFound:
            embedError = discord.Embed()
            embedError.description = "It seems like there are no quests with that name on the server. Please try again"
            await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @questsDelete.command(name="one")
    async def deleteOneQuest(self, ctx, *, name: Option(str, "The name of the quest")):
        """Deletes one quest"""
        mainRes = await questsUtil.getUserQuestOne(
            guild_id=ctx.guild.id, user_id=ctx.author.id, name=name, uri=CONNECTION_URI
        )
        questUUID = dict(mainRes)["uuid"]
        await questsUtil.deleteOneQuest(
            guild_id=ctx.guild.id,
            user_id=ctx.author.id,
            uuid=questUUID,
            uri=CONNECTION_URI,
        )
        await ctx.respond(f"Quest {name} has been deleted")

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @questsDelete.command(name="all")
    async def deleteAllUserQuests(self, ctx):
        """Deletes all of the quests belonging to you"""
        embed = discord.Embed()
        embed.description = (
            "Are you sure you want to delete all of your quests? This cannot be undone"
        )
        await ctx.respond(embed=embed, view=DeleteAllView(), ephemeral=True)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(ServerQuests(bot))
