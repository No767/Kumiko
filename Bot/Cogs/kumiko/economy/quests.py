import asyncio
import os

import discord
import uvloop
from dateutil import parser
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands, pages
from dotenv import load_dotenv
from kumiko_economy import KumikoEcoUserUtils, KumikoQuestsUtils
from kumiko_ui_components import (
    QuestsCreateModal,
    QuestsDeleteOneConfirmView,
    QuestsPurgeAllView,
    QuestsUpdateTimeModal,
)
from rin_exceptions import ItemNotFound

load_dotenv()

POSTGRES_PASSWORD = os.getenv("Postgres_Password")
POSTGRES_SERVER_IP = os.getenv("Postgres_Server_IP")
POSTGRES_DB = os.getenv("Postgres_Kumiko_Database")
POSTGRES_PORT = os.getenv("Postgres_Port")
POSTGRES_USERNAME = os.getenv("Postgres_Username")
CONNECTION_URI = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:{POSTGRES_PORT}/{POSTGRES_DB}"
USERS_CONNECTION_URI = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:{POSTGRES_PORT}/{POSTGRES_DB}"

questsUtil = KumikoQuestsUtils()
userUtils = KumikoEcoUserUtils()


class EcoQuests(commands.Cog):
    """Kumiko Quests - A fun way to earn some Petals"""

    def __init__(self, bot):
        self.bot = bot

    quests = SlashCommandGroup(
        "eco-quests", "Commands for the quests feature in Kumiko"
    )
    questsDelete = quests.create_subgroup("delete", "deletes quests")

    @quests.command(name="create")
    @commands.cooldown(1, 7200, commands.BucketType.user)
    async def createQuests(self, ctx):
        """Creates a quest"""
        createModal = QuestsCreateModal(uri=CONNECTION_URI, title="Create a quest")
        await ctx.send_modal(createModal)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @quests.command(name="view")
    async def viewQuest(
        self,
        ctx,
        *,
        filters: Option(
            str,
            "Filters for viewing quests",
            choices=["All", "Active", "Inactive", "Claimed", "Unclaimed"],
        ),
    ):
        """Views quests"""
        questsData = await questsUtil.getAllQuests(uri=CONNECTION_URI)
        userRank = await userUtils.selectUserRank(
            user_id=ctx.author.id, uri=USERS_CONNECTION_URI
        )
        if filters in ["All"]:
            questsData = await questsUtil.getAllQuests(uri=CONNECTION_URI)
        elif filters in ["Active"]:
            questsData = await questsUtil.getActiveQuests(
                active=True, uri=CONNECTION_URI
            )
        elif filters in ["Inactive"]:
            questsData = await questsUtil.getActiveQuests(
                active=False, uri=CONNECTION_URI
            )
        elif filters in ["Claimed"]:
            questsData = await questsUtil.viewClaimedQuests(
                claimed=True, uri=CONNECTION_URI
            )
        elif filters in ["Unclaimed"]:
            questsData = await questsUtil.viewClaimedQuests(
                claimed=False, uri=CONNECTION_URI
            )
        else:
            questsData = await questsUtil.getAllQuests(uri=CONNECTION_URI)

        try:
            if len(questsData) == 0:
                raise ItemNotFound
            else:
                for items in userRank:
                    if int(items) < 5:
                        await ctx.respond(
                            f"Sorry, but you can't use the quests feature since you are current rank is {items}"
                        )
                    else:
                        mainPages = pages.Paginator(
                            pages=[
                                discord.Embed(
                                    title=dict(items)["name"],
                                    description=dict(items)["description"],
                                )
                                .add_field(
                                    name="Reward",
                                    value=dict(items)["reward"],
                                    inline=True,
                                )
                                .add_field(
                                    name="End Date",
                                    value=parser.isoparse(
                                        dict(items)["end_datetime"]
                                    ).strftime("%Y-%m-%d %H:%M:%S"),
                                    inline=True,
                                )
                                .add_field(
                                    name="Creator",
                                    value=f'{await self.bot.get_or_fetch_user(dict(items)["creator"])}',
                                    inline=True,
                                )
                                .add_field(
                                    name="Date Created",
                                    value=parser.isoparse(
                                        dict(items)["date_created"]
                                    ).strftime("%Y-%m-%d %H:%M:%S"),
                                    inline=True,
                                )
                                .add_field(
                                    name="Active?",
                                    value=dict(items)["active"],
                                    inline=True,
                                )
                                .add_field(
                                    name="Claimed by",
                                    value=await self.bot.get_or_fetch_user(
                                        dict(items)["claimed_by"]
                                    )
                                    if dict(items)["claimed_by"] is not None
                                    else "None",
                                    inline=True,
                                )
                                for items in questsData
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

    @quests.command(name="update")
    @commands.cooldown(1, 7200, commands.BucketType.user)
    async def updateQuests(
        self,
        ctx,
    ):
        """Updates the quest with new info"""
        mainModal = QuestsUpdateTimeModal(uri=CONNECTION_URI, title="Update Quest")
        await ctx.send_modal(mainModal)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @questsDelete.command(name="one")
    async def deleteOneQuest(self, ctx):
        """Deletes one quest"""
        embed = discord.Embed()
        embed.description = "Are you sure you wish to delete that quest?"
        await ctx.respond(
            embed=embed,
            view=QuestsDeleteOneConfirmView(uri=CONNECTION_URI),
            ephemeral=True,
        )

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @questsDelete.command(name="all")
    async def deleteAllUserQuests(self, ctx):
        """Deletes all of the quests belonging to you"""
        embed = discord.Embed()
        embed.description = (
            "Are you sure you want to delete all of your quests? This cannot be undone"
        )
        await ctx.respond(
            embed=embed,
            view=QuestsPurgeAllView(user_uri=CONNECTION_URI, quests_uri=CONNECTION_URI),
            ephemeral=True,
        )

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @quests.command(name="claim")
    @commands.cooldown(1, 7200, commands.BucketType.user)
    async def claimQuest(self, ctx, *, name: Option(str, "The name of the quest")):
        """Allows you to claim a quest"""
        questNameData = await questsUtil.getQuestViaName(name=name, uri=CONNECTION_URI)
        userRank = await userUtils.selectUserRank(
            user_id=ctx.author.id, uri=USERS_CONNECTION_URI
        )
        try:
            if len(questNameData) == 0 or len(userRank) == 0:
                raise ItemNotFound
            else:
                for items in userRank:
                    if int(items) < 5:
                        await ctx.respond(
                            f"Sorry, but you can't use the quests feature since you are current rank is {items}"
                        )
                    else:
                        for questItem in questNameData:
                            questItemMain = dict(questItem)
                            questItemUUID = questItemMain["uuid"]
                            questItemUserID = questItemMain["creator"]
                            questItemClaimedBy = questItemMain["claimed_by"]
                        if questItemClaimedBy is None:
                            await questsUtil.claimQuest(
                                user_id=questItemUserID,
                                claimer_id=ctx.user.id,
                                uuid=questItemUUID,
                                claimed=True,
                                uri=CONNECTION_URI,
                            )
                            await ctx.respond(f"You have claimed {name}")
                        else:
                            await ctx.respond(
                                f"The quest has been already claimed. Please select another one"
                            )
        except ItemNotFound:
            embedError = discord.Embed()
            embedError.description = "It seems like there are no quests with that name (or you haven't created an account yet). Please try again"
            await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @quests.command(name="unclaim")
    @commands.cooldown(1, 7200, commands.BucketType.user)
    async def unclaimQuest(self, ctx, *, name: Option(str, "The name of the quest")):
        """Unclaims a quest that you claimed"""
        questNameData = await questsUtil.getQuestViaName(name=name, uri=CONNECTION_URI)
        userRank = await userUtils.selectUserRank(
            user_id=ctx.author.id, uri=USERS_CONNECTION_URI
        )
        try:
            if len(questNameData) == 0 or len(userRank) == 0:
                raise ItemNotFound
            else:
                for questItem in questNameData:
                    questItemMain = dict(questItem)
                for items in userRank:
                    if int(items) < 5:
                        await ctx.respond(
                            f"Sorry, but you can't use the quests feature since you are current rank is {items}"
                        )
                    else:
                        if (
                            questItemMain["claimed_by"] is not None
                            and int(questItemMain["claimed_by"]) == ctx.author.id
                        ):
                            await questsUtil.claimQuest(
                                user_id=questItemMain["creator"],
                                claimer_id=None,
                                uuid=questItemMain["uuid"],
                                claimed=False,
                                uri=CONNECTION_URI,
                            )
                            await ctx.respond(
                                f"You have successfully unclaimed the quest {questItemMain['name']}"
                            )
                        else:
                            await ctx.respond(
                                "That quest you requested hasn't been claimed yet. Go ahead and claim it!"
                            )
        except ItemNotFound:
            embedError = discord.Embed()
            embedError.description = "It seems like there are no quests with that name (or you haven't created an account yet). Please try again"
            await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(EcoQuests(bot))
