import asyncio
import os
import urllib.parse
from datetime import datetime

import discord
import uvloop
from dateutil import parser
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands, pages
from dotenv import load_dotenv
from genshin_wish_sim_utils import (
    KumikoWSUserInvUtils,
    KumikoWSUsersUtils,
    KumikoWSUtils,
)
from kumiko_genshin_wish_sim import KumikoGWSUtils, WSUser, WSUserInv
from kumiko_ui_components import GWSDeleteOneInvView, GWSPurgeAllInvView
from kumiko_utils import KumikoCM
from rin_exceptions import ItemNotFound, NoItemsError

load_dotenv()

POSTGRES_PASSWORD = urllib.parse.quote_plus(os.getenv("Postgres_Password"))
POSTGRES_SERVER_IP = os.getenv("Postgres_Server_IP")
POSTGRES_WS_DATABASE = os.getenv("Postgres_Kumiko_Database")
POSTGRES_USERNAME = os.getenv("Postgres_Username")
POSTGRES_PORT = os.getenv("Postgres_Port")
WS_CONNECTION_URI = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:{POSTGRES_PORT}/{POSTGRES_WS_DATABASE}"
CONNECTION_URI = f"asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:{POSTGRES_PORT}/{POSTGRES_WS_DATABASE}"
MODELS = ["kumiko_genshin_wish_sim.models"]

wsUtils = KumikoWSUtils()
wsUserInvUtils = KumikoWSUserInvUtils()
wsUserUtils = KumikoWSUsersUtils()

gwsUtils = KumikoGWSUtils(uri=CONNECTION_URI, models=MODELS)


class GWS(commands.Cog):
    """Kumiko's Genshin Wish Simulator (GWS)"""

    def __init__(self, bot):
        self.bot = bot

    gws = SlashCommandGroup("gws", "Commands for Kumiko's Genshin Wish Sim")
    gwsWish = gws.create_subgroup("wish", "Wish for some items")

    gwsUserInvDelete = gws.create_subgroup("delete", "Deletes some stuff from your inv")

    @gwsWish.command(name="improved-one")
    async def improvedGwsWishOne(self, ctx: discord.ApplicationContext):
        """Improved version of the wish command"""
        async with KumikoCM(uri=CONNECTION_URI, models=MODELS):
            userProfileExists = await WSUser.filter(user_id=ctx.user.id).exists()
            userInvExists = await WSUserInv.filter(user_id=ctx.user.id).exists()
            pulls = 0
            totalPulls = 0
            if userProfileExists is False:
                await WSUser.create(
                    user_id=ctx.user.id,
                    username=ctx.user.name,
                    pulls=pulls,
                    date_joined=discord.utils.utcnow().isoformat(),
                )
                totalPulls = pulls + 1
            else:
                # TODO: Add a cache check here (w/ Redis)
                userProfile = await WSUser.filter(user_id=ctx.user.id).first().values()
                pulls = userProfile["pulls"]
                totalPulls = userProfile["pulls"] + 1

            starRank = (
                4
                if pulls % 10 == 0
                else (5 if pulls % 90 == 0 else await gwsUtils.determineStarRank())
            )
            await WSUser.filter(user_id=ctx.user.id).update(pulls=totalPulls)
            wishItem = await gwsUtils.getWish(star_rank=starRank, size=1)

            if userInvExists is False:
                await WSUserInv.create(
                    item_uuid=wishItem["uuid"],
                    user_id=ctx.user.id,
                    date_obtained=discord.utils.utcnow().isoformat(),
                    name=wishItem["name"],
                    description=wishItem["description"],
                    star_rank=wishItem["star_rank"],
                    type=wishItem["type"],
                    amount=1,
                )
            else:
                itemInInv = (
                    await WSUserInv.filter(
                        user_id=ctx.user.id, item_uuid=wishItem["uuid"]
                    )
                    .first()
                    .values()
                )
                if itemInInv is None:
                    await WSUserInv.create(
                        item_uuid=wishItem["uuid"],
                        user_id=ctx.user.id,
                        date_obtained=discord.utils.utcnow().isoformat(),
                        name=wishItem["name"],
                        description=wishItem["description"],
                        star_rank=wishItem["star_rank"],
                        type=wishItem["type"],
                        amount=1,
                    )
                else:
                    totalAmount = itemInInv["amount"] + 1
                    await WSUserInv.filter(
                        user_id=ctx.user.id, item_uuid=wishItem["uuid"]
                    ).update(amount=totalAmount)

            embed = discord.Embed()
            embed.title = wishItem["name"]
            embed.description = wishItem["description"]
            embed.add_field(name="Star Rank", value=wishItem["star_rank"])
            embed.add_field(name="Type", value=wishItem["type"])
            embed.set_image(
                url=f"https://raw.githubusercontent.com/No767/Kumiko-WS-Assets/master/assets/{wishItem['uuid']}.png"
            )
            await ctx.respond(embed=embed)

    @gwsWish.command(name="one")
    async def gwsWishOne(self, ctx: discord.ApplicationContext):
        """Allows you to wish for one item"""
        await ctx.defer()
        getUserProfile = await wsUserUtils.getFirstUser(
            user_id=ctx.author.id, uri=WS_CONNECTION_URI
        )
        starRank = 3

        if getUserProfile is None:
            await wsUserUtils.insertNewUser(
                user_id=ctx.user.id,
                username=ctx.user.name,
                pulls=0,
                date_joined=discord.utils.utcnow().isoformat(),
                uri=WS_CONNECTION_URI,
            )
            getUserProfile = await wsUserUtils.getFirstUser(
                user_id=ctx.author.id, uri=WS_CONNECTION_URI
            )

        if int(dict(getUserProfile[0])["pulls"]) % 10 == 0:
            starRank = 4
        elif int(dict(getUserProfile[0])["pulls"]) % 90 == 0:
            starRank = 5
        else:
            starRank = await wsUtils.determineStarRank()

        totalAmount = int(dict(getUserProfile[0])["pulls"]) + 1
        await wsUserUtils.updateUserPullCount(
            user_id=ctx.author.id, amount=totalAmount, uri=WS_CONNECTION_URI
        )
        mainRes = await wsUtils.getRandomWSArray(
            star_rank=starRank, uri=WS_CONNECTION_URI
        )
        mainResDict = dict(mainRes)
        embed = discord.Embed()

        checkUserInv = await wsUserInvUtils.getUserInv(
            user_id=ctx.author.id, uri=WS_CONNECTION_URI
        )
        if len(checkUserInv) == 0:
            await wsUserInvUtils.insertWSItemToUserInv(
                uuid=mainResDict["uuid"],
                user_id=ctx.author.id,
                date_obtained=datetime.now().isoformat(),
                name=mainResDict["name"],
                description=mainResDict["description"],
                star_rank=mainResDict["star_rank"],
                type=mainResDict["type"],
                amount=1,
                uri=WS_CONNECTION_URI,
            )
        else:
            doesItemExistInUserInv = await wsUserInvUtils.getIfItemExistsInUserInv(
                user_id=ctx.author.id,
                uuid=mainResDict["uuid"],
                uri=WS_CONNECTION_URI,
            )
            getItem = await wsUserInvUtils.searchItemUUIDInInv(
                user_id=ctx.author.id, uuid=mainResDict["uuid"], uri=WS_CONNECTION_URI
            )
            if doesItemExistInUserInv is True:
                totalAmount = dict(getItem)["amount"] + 1
                await wsUserInvUtils.updateWSItemAmount(
                    user_id=ctx.author.id,
                    uuid=mainResDict["uuid"],
                    amount=totalAmount,
                    uri=WS_CONNECTION_URI,
                )
            else:
                await wsUserInvUtils.insertWSItemToUserInv(
                    uuid=mainResDict["uuid"],
                    user_id=ctx.author.id,
                    date_obtained=discord.utils.utcnow().isoformat(),
                    name=mainResDict["name"],
                    description=mainResDict["description"],
                    star_rank=mainResDict["star_rank"],
                    type=mainResDict["type"],
                    amount=1,
                    uri=WS_CONNECTION_URI,
                )

        embed.title = mainResDict["name"]
        embed.description = mainResDict["description"]
        embed.add_field(name="Star Rank", value=mainResDict["star_rank"], inline=True)
        embed.add_field(name="Type", value=mainResDict["type"], inline=True)
        embed.set_image(
            url=f"https://raw.githubusercontent.com/No767/Kumiko-WS-Assets/master/assets/{mainResDict['uuid']}.png"
        )
        await ctx.send_followup(embed=embed)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @gwsWish.command(name="multiple")
    async def gwsWishMultiple(
        self,
        ctx: discord.ApplicationContext,
        *,
        num_of_wishes: Option(
            int, "The number of wishes to perform", min_value=1, max_value=10
        ),
    ):
        """Allows you to wish for up to 10 items at once"""
        await ctx.defer()
        getUserProfile = await wsUserUtils.getFirstUser(
            user_id=ctx.author.id, uri=WS_CONNECTION_URI
        )
        starRank = 3
        if getUserProfile is None:
            await wsUserUtils.insertNewUser(
                user_id=ctx.user.id,
                username=ctx.user.name,
                pulls=0,
                date_joined=discord.utils.utcnow().isoformat(),
                uri=WS_CONNECTION_URI,
            )
            getUserProfile = await wsUserUtils.getFirstUser(
                user_id=ctx.author.id, uri=WS_CONNECTION_URI
            )

        if int(dict(getUserProfile[0])["pulls"]) % 10 == 0:
            starRank = 4
        elif int(dict(getUserProfile[0])["pulls"]) % 90 == 0:
            starRank = 5
        else:
            starRank = await wsUtils.determineStarRank()

        totalAmount = int(dict(getUserProfile[0])["pulls"]) + num_of_wishes

        await wsUserUtils.updateUserPullCount(
            user_id=ctx.user.id, amount=totalAmount, uri=WS_CONNECTION_URI
        )
        mainRes = await wsUtils.getRandomWSItemMultiple(
            amount=num_of_wishes, star_rank=starRank, uri=WS_CONNECTION_URI
        )
        checkUserInv = await wsUserInvUtils.getUserInv(
            user_id=ctx.author.id, uri=WS_CONNECTION_URI
        )
        if len(checkUserInv) == 0:
            for items in mainRes:
                await wsUserInvUtils.insertWSItemToUserInv(
                    uuid=dict(items)["uuid"],
                    user_id=ctx.author.id,
                    date_obtained=datetime.now().isoformat(),
                    name=dict(items)["name"],
                    description=dict(items)["description"],
                    star_rank=dict(items)["star_rank"],
                    type=dict(items)["type"],
                    amount=1,
                    uri=WS_CONNECTION_URI,
                )
        else:
            for mainItems in mainRes:
                itemExistsInUserInv = await wsUserInvUtils.getIfItemExistsInUserInv(
                    user_id=ctx.author.id,
                    uuid=dict(mainItems)["uuid"],
                    uri=WS_CONNECTION_URI,
                )
                if itemExistsInUserInv is True:
                    getItem = await wsUserInvUtils.searchItemUUIDInInv(
                        user_id=ctx.author.id,
                        uuid=dict(mainItems)["uuid"],
                        uri=WS_CONNECTION_URI,
                    )
                    totalAmount = dict(getItem)["amount"] + 1
                    await wsUserInvUtils.updateWSItemAmount(
                        user_id=ctx.author.id,
                        uuid=dict(mainItems)["uuid"],
                        amount=totalAmount,
                        uri=WS_CONNECTION_URI,
                    )
                else:
                    await wsUserInvUtils.insertWSItemToUserInv(
                        uuid=dict(mainItems)["uuid"],
                        user_id=ctx.author.id,
                        date_obtained=discord.utils.utcnow().isoformat(),
                        name=dict(mainItems)["name"],
                        description=dict(mainItems)["description"],
                        star_rank=dict(mainItems)["star_rank"],
                        type=dict(mainItems)["type"],
                        amount=1,
                        uri=WS_CONNECTION_URI,
                    )
        mainPages = pages.Paginator(
            pages=[
                discord.Embed(
                    title=dict(item2)["name"], description=dict(item2)["description"]
                )
                .add_field(
                    name="Star Rank", value=dict(item2)["star_rank"], inline=True
                )
                .add_field(name="Type", value=dict(item2)["type"], inline=True)
                .set_image(
                    url=f"https://raw.githubusercontent.com/No767/Kumiko-WS-Assets/master/assets/{dict(item2)['uuid']}.png"
                )
                for item2 in mainRes
            ],
            loop_pages=True,
        )
        await mainPages.respond(ctx.interaction, ephemeral=False)

    @gws.command(name="inv")
    async def accessUserInv(self, ctx):
        """Accesses your inventory for GWS"""
        userInv = await wsUserInvUtils.getUserInv(
            user_id=ctx.author.id, uri=WS_CONNECTION_URI
        )
        try:
            if len(userInv) == 0:
                raise NoItemsError
            else:
                mainPages = pages.Paginator(
                    pages=[
                        discord.Embed(
                            title=dict(mainItem)["name"],
                            description=dict(mainItem)["description"],
                        )
                        .add_field(
                            name="Date Obtained",
                            value=parser.isoparse(
                                dict(mainItem)["date_obtained"]
                            ).strftime("%Y-%m-%d %H:%M:%S"),
                            inline=True,
                        )
                        .add_field(
                            name="Star Rank",
                            value=dict(mainItem)["star_rank"],
                            inline=True,
                        )
                        .add_field(
                            name="Type", value=dict(mainItem)["type"], inline=True
                        )
                        .add_field(
                            name="Amount", value=dict(mainItem)["amount"], inline=True
                        )
                        .set_image(
                            url=f"https://raw.githubusercontent.com/No767/Kumiko-WS-Assets/master/assets/{dict(mainItem)['item_uuid']}.png"
                        )
                        for mainItem in userInv
                    ],
                    loop_pages=True,
                )
                await mainPages.respond(ctx.interaction, ephemeral=False)
        except NoItemsError:
            embedError = discord.Embed()
            embedError.description = "Sorry, but it seems like there are no items in your inventory. Please try again"
            await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @gwsUserInvDelete.command(name="one")
    async def deleteOneUserInv(self, ctx):
        """Deletes one item from your inventory"""
        embed = discord.Embed()
        embed.description = "Are you sure you want to delete this item?"
        await ctx.respond(
            embed=embed, view=GWSDeleteOneInvView(uri=WS_CONNECTION_URI), ephemeral=True
        )

    @gwsUserInvDelete.command(name="all")
    async def purgeUserInv(self, ctx):
        """Deletes all of your items in your GWS inventory"""
        embed = discord.Embed()
        embed.description = "Do you want to purge all of the items from your user inventory? This cannot be undone"
        await ctx.respond(
            embed=embed, view=GWSPurgeAllInvView(uri=WS_CONNECTION_URI), ephemeral=True
        )

    @gws.command(name="profile")
    async def getUserProfile(self, ctx):
        """Gets your GWS profile"""
        mainRes = await wsUserUtils.getFirstUser(
            user_id=ctx.author.id, uri=WS_CONNECTION_URI
        )
        try:
            if mainRes is None:
                raise ItemNotFound
            else:
                user = dict(mainRes[0])
                getUserInfo = await self.bot.get_or_fetch_user(user["user_id"])
                embed = discord.Embed()
                embed.title = f"{user['username']}'s Profile"
                embed.add_field(name="Pulls", value=user["pulls"], inline=True)
                embed.add_field(
                    name="Date Joined",
                    value=parser.isoparse(user["date_joined"]).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    inline=True,
                )
                embed.set_thumbnail(url=getUserInfo.display_avatar.url)
                await ctx.respond(embed=embed, ephemeral=True)
        except ItemNotFound:
            embedError = discord.Embed()
            embedError.description = "Sorry, but it seems like you don't have a profile. Make a pull to create one"
            await ctx.respond(embed=embedError, ephemeral=True)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(GWS(bot))
