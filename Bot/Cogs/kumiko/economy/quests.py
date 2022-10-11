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
from economy_utils import KumikoEcoUserUtils, KumikoQuestsUtils
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
            user_id=interaction.user.id,
            uri=CONNECTION_URI,
        )
        userRank = await userUtils.selectUserRank(
            user_id=interaction.user.id, uri=USERS_CONNECTION_URI
        )
        try:
            if len(itemUUIDAuth) == 0:
                raise ItemNotFound
            else:
                for rank in userRank:
                    if int(rank) < 5:
                        await interaction.reponse.send_message(
                            f"Sorry, but you can't use the quests feature since you are current rank is {rank}",
                            ephemeral=True,
                        )
                    else:
                        for item in itemUUIDAuth:
                            await questsUtil.purgeUserQuests(
                                user_id=interaction.user.id,
                                uuid=item,
                                uri=CONNECTION_URI,
                            )
                        await interaction.response.send_message(
                            "All quests belonging to you have been purged.",
                            ephemeral=True,
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


class EcoQuests(commands.Cog):
    """Kumiko Quests - A fun way to earn some Petals"""

    def __init__(self, bot):
        self.bot = bot

    quests = SlashCommandGroup(
        "eco-quests",
        "Commands for the quests feature in Kumiko",
        guild_ids=[970159505390325842],
    )
    questsDelete = quests.create_subgroup(
        "delete", "deletes quests", guild_ids=[970159505390325842]
    )

    @quests.command(name="create")
    @commands.cooldown(1, 7200, commands.BucketType.user)
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
        getUser = await userUtils.getFirstUser(user_id=ctx.user.id, uri=CONNECTION_URI)

        if getUser is None:
            await ctx.respond("Probably should create an account first...")

        elif int(dict(getUser)["rank"]) < 5:
            await ctx.respond(
                f"Sorry, but you can't use the quests feature since you are current rank is {dict(getUser)['rank']}"
            )
        else:
            questUUIDItem = str(uuid.uuid4())
            dateCreated = datetime.now().isoformat()
            endDateFormatted = parser.parse(f"{end_date} {end_time}").isoformat()
            totalUserPetals = int(dict(getUser)["lavender_petals"]) - int(reward)
            await userUtils.updateUserLavenderPetals(
                user_id=ctx.user.id,
                lavender_petals=totalUserPetals,
                uri=USERS_CONNECTION_URI,
            )
            await questsUtil.createQuests(
                uuid=questUUIDItem,
                creator=ctx.author.id,
                claimed_by=None,
                date_created=dateCreated,
                end_datetime=endDateFormatted,
                name=name,
                description=description,
                reward=reward,
                active=True,
                claimed=False,
                uri=CONNECTION_URI,
            )
            await ctx.respond(f"Created quest: {name}")

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
        *,
        name: Option(str, "The name of the quest"),
        reward: Option(int, "The new reward to update to"),
        end_date: Option(str, "The new date to update to"),
        end_time: Option(str, "The new time to update to"),
    ):
        """Updates the quest with new info"""
        mainQuest = await questsUtil.getQuestViaName(
            user_id=ctx.user.id, name=name, uri=CONNECTION_URI
        )
        mainUserData = await userUtils.obtainUserData(
            user_id=ctx.user.id, uri=USERS_CONNECTION_URI
        )
        try:
            if len(mainQuest) == 0 or len(mainUserData) == 0:
                raise ItemNotFound
            else:
                fullDateTime = parser.parse(f"{end_date} {end_time}").isoformat()
                for userData in mainUserData:
                    currentUserPetals = dict(userData)["lavender_petals"]
                    currentUserRank = dict(userData)["rank"]
                totalUserPetals = currentUserPetals - reward
                if currentUserRank < 5:
                    await ctx.respond(
                        f"Sorry, but you can't use the quests feature since you are current rank is {currentUserRank}"
                    )
                else:
                    await userUtils.updateUserLavenderPetals(
                        user_id=ctx.user.id,
                        lavender_petals=totalUserPetals,
                        uri=USERS_CONNECTION_URI,
                    )
                    for items in mainQuest:
                        await questsUtil.updateQuest(
                            uuid=dict(items)["uuid"],
                            reward=reward,
                            new_end_datetime=fullDateTime,
                            uri=CONNECTION_URI,
                        )
                        await ctx.respond(f"Updated {name} with an reward of {reward}")
        except ItemNotFound:
            embedError = discord.Embed()
            embedError.description = "It seems like there are no quests with that name (or you haven't created an account yet). Please try again"
            await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @questsDelete.command(name="one")
    async def deleteOneQuest(self, ctx, *, name: Option(str, "The name of the quest")):
        """Deletes one quest"""
        mainRes = await questsUtil.getUserQuestOne(
            user_id=ctx.author.id, name=name, uri=CONNECTION_URI
        )
        userRank = await userUtils.selectUserRank(
            user_id=ctx.author.id, uri=USERS_CONNECTION_URI
        )
        questUUID = dict(mainRes)["uuid"]
        try:
            if len(userRank) == 0:
                raise ItemNotFound
            else:
                for items in userRank:
                    if int(items) < 5:
                        await ctx.respond(
                            f"Sorry, but you can't use the quests feature since you are current rank is {items}"
                        )
                    else:
                        await questsUtil.deleteOneQuest(
                            user_id=ctx.author.id,
                            uuid=questUUID,
                            uri=CONNECTION_URI,
                        )
                        await ctx.respond(f"Quest {name} has been deleted")
        except ItemNotFound:
            embedError = discord.Embed()
            embedError.description = "It seems like you either don't have an account yet, or the the quest you requested is not found. Please try again"
            await ctx.respond(embed=embedError)

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

    @quests.command(name="reward")
    async def giveQuestsReward(
        self, ctx, *, name: Option(str, "The name of the quest")
    ):
        """Alow you to give the reward for the quest"""
        questData = await questsUtil.getQuestViaName(name=name, uri=CONNECTION_URI)
        userData = await userUtils.obtainUserData(
            user_id=ctx.author.id, uri=USERS_CONNECTION_URI
        )
        try:
            if len(questData) == 0 or len(userData) == 0:
                raise ItemNotFound
            else:
                for items in userData:
                    mainItems = dict(items)
                    if int(dict(items)["rank"]) < 5:
                        await ctx.respond(
                            f"Sorry, but you can't use the quests feature since you are current rank is {mainItems['rank']}"
                        )
                    else:
                        for questItem in questData:
                            mainItem = dict(questItem)
                            creatorID = mainItem["creator"]
                            claimedUserID = mainItem["claimed_by"]
                            totalPetalsCreator = (
                                mainItems["lavender_petals"] - mainItem["reward"]
                            )
                            if claimedUserID is None:
                                await ctx.respond(
                                    "Sorry, you can't reward the quest, since someone has not claimed it yet. Please try again"
                                )
                            else:
                                claimedUserData = await userUtils.obtainUserData(
                                    user_id=claimedUserID, uri=USERS_CONNECTION_URI
                                )
                                for data in claimedUserData:
                                    claimedUserCurrentPetals = dict(data)[
                                        "lavender_petals"
                                    ]
                                claimedTotalReward = (
                                    int(claimedUserCurrentPetals) + mainItem["reward"]
                                )
                                await userUtils.updateUserLavenderPetals(
                                    user_id=creatorID,
                                    lavender_petals=totalPetalsCreator,
                                    uri=USERS_CONNECTION_URI,
                                )
                                await userUtils.updateUserLavenderPetals(
                                    user_id=claimedUserID,
                                    lavender_petals=claimedTotalReward,
                                    uri=USERS_CONNECTION_URI,
                                )
                                await questsUtil.setQuestActiveStatus(
                                    uuid=mainItem["uuid"],
                                    active=False,
                                    uri=CONNECTION_URI,
                                )
                                await ctx.respond("The quest has been rewarded")
        except ItemNotFound:
            embedError = discord.Embed()
            embedError.description = "It seems like there are no quests on the server (or you haven't made an account yet). Please try again"
            await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(EcoQuests(bot))
