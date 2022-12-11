import os
import urllib.parse

import discord
from dateutil import parser
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands, pages
from dotenv import load_dotenv
from kumiko_genshin_wish_sim import (
    KumikoGWSCacheUtils,
    KumikoGWSUtils,
    WSUser,
    WSUserInv,
)
from kumiko_ui_components import GWSDeleteOneUserInvItemModal, GWSPurgeInvView
from kumiko_utils import KumikoCM
from rin_exceptions import ItemNotFound, NoItemsError

load_dotenv()

REDIS_HOST = os.getenv("Redis_Server_IP")
REDIS_PORT = os.getenv("Redis_Port")
POSTGRES_PASSWORD = urllib.parse.quote_plus(os.getenv("Postgres_Password"))
POSTGRES_SERVER_IP = os.getenv("Postgres_Server_IP")
POSTGRES_WS_DATABASE = os.getenv("Postgres_Kumiko_Database")
POSTGRES_USERNAME = os.getenv("Postgres_Username")
POSTGRES_PORT = os.getenv("Postgres_Port")
CONNECTION_URI = f"asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:{POSTGRES_PORT}/{POSTGRES_WS_DATABASE}"
MODELS = ["kumiko_genshin_wish_sim.models"]

gwsUtils = KumikoGWSUtils(uri=CONNECTION_URI, models=MODELS)
cacheUtils = KumikoGWSCacheUtils(
    uri=CONNECTION_URI, models=MODELS, redis_host=REDIS_HOST, redis_port=REDIS_PORT
)


class GWS(commands.Cog):
    """Kumiko's Genshin Wish Simulator (GWS)"""

    def __init__(self, bot):
        self.bot = bot

    gws = SlashCommandGroup("gws", "Commands for Kumiko's Genshin Wish Sim")
    gwsWish = gws.create_subgroup("wish", "Wish for some items")
    gwsUserInvDelete = gws.create_subgroup("delete", "Deletes some stuff from your inv")

    @gwsWish.command(name="one")
    async def gwsWishOne(self, ctx: discord.ApplicationContext):
        """Allows you to wish for one item"""
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

    @gwsWish.command(name="multiple")
    async def gwsWishMultiple(
        self,
        ctx: discord.ApplicationContext,
        *,
        number_of_wishes: Option(
            int, "How much wishes do you wish to make?", min_value=2, max_value=10
        ),
    ):
        """Allows you to wish for up to 10 items at once"""
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
                totalPulls = pulls + number_of_wishes
            else:
                userProfile = await WSUser.filter(user_id=ctx.user.id).first().values()
                pulls = userProfile["pulls"]
                totalPulls = userProfile["pulls"] + number_of_wishes

            starRank = (
                4
                if pulls % 10 == 0
                else (5 if pulls % 90 == 0 else await gwsUtils.determineStarRank())
            )
            await WSUser.filter(user_id=ctx.user.id).update(pulls=totalPulls)
            wishItemArr = await gwsUtils.getWish(
                star_rank=starRank, size=number_of_wishes
            )

            if userInvExists is False:
                for wishItem in wishItemArr:
                    await WSUSerInv.create(
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
                for wishItem in wishItemArr:
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

            mainPages = pages.Paginator(
                pages=[
                    discord.Embed(title=item["name"], description=item["description"])
                    .add_field(name="Star Rank", value=item["star_rank"])
                    .add_field(name="Type", value=item["type"])
                    .set_image(
                        url=f"https://raw.githubusercontent.com/No767/Kumiko-WS-Assets/master/assets/{item['uuid']}.png"
                    )
                    for item in wishItemArr
                ],
                loop_pages=True,
            )

            await mainPages.respond(ctx.interaction, ephemeral=False)

    @gws.command(name="inv")
    async def gwsUserInv(self, ctx):
        """Allows you to view your inventory"""
        userInv = await cacheUtils.cacheUserInv(
            user_id=ctx.user.id, command_name=ctx.command.qualified_name
        )
        try:
            if userInv is None:
                raise NoItemsError
            else:
                mainPages = pages.Paginator(
                    pages=[
                        discord.Embed(
                            title=items["name"], description=items["description"]
                        )
                        .add_field(
                            name="Date Obtained",
                            value=discord.utils.format_dt(
                                parser.isoparse(items["date_obtained"]), style="F"
                            ),
                        )
                        .add_field(name="Star Rank", value=items["star_rank"])
                        .add_field(name="Type", value=items["type"])
                        .add_field(name="Amount", value=items["amount"])
                        .set_image(
                            url=f"https://raw.githubusercontent.com/No767/Kumiko-WS-Assets/master/assets/{items['item_uuid']}.png"
                        )
                        for items in userInv
                    ],
                    loop_pages=True,
                )
                await mainPages.respond(ctx.interaction, ephemeral=False)
        except NoItemsError:
            embedError = discord.Embed()
            embedError.description = "Sorry, but it seems like there are no items in your inventory. Please try again"
            await ctx.respond(embed=embedError)

    @gwsUserInvDelete.command(name="one")
    async def deleteOneUserInv(self, ctx: discord.ApplicationContext):
        """Deletes one item from your inventory"""
        view = GWSDeleteOneUserInvItemModal(
            uri=CONNECTION_URI,
            models=MODELS,
            redis_host=REDIS_HOST,
            redis_port=REDIS_PORT,
            command_name=ctx.command.qualified_name,
            title="Delete One Item",
        )
        await ctx.send_modal(view)

    @gwsUserInvDelete.command(name="all")
    async def purgeUserInv(self, ctx):
        """Deletes all of your items in your GWS inventory"""
        embed = discord.Embed()
        embed.description = "Do you want to purge all of the items from your user inventory? This cannot be undone"
        await ctx.respond(
            embed=embed,
            view=GWSPurgeInvView(uri=CONNECTION_URI, models=MODELS),
            ephemeral=True,
        )

    @gws.command(name="profile")
    async def getUserProfile(self, ctx):
        """Gets your GWS profile"""
        async with KumikoCM(uri=CONNECTION_URI, models=MODELS):
            getUserProfile = await cacheUtils.cacheUser(
                user_id=ctx.user.id, command_name=ctx.command.qualified_name
            )
            try:
                if getUserProfile is None:
                    raise ItemNotFound
                else:
                    getUserInfo = await self.bot.get_or_fetch_user(
                        getUserProfile["user_id"]
                    )
                    embed = discord.Embed()
                    embed.title = f"{getUserProfile['username']}'s Profile"
                    embed.add_field(name="Pulls", value=getUserProfile["pulls"])
                    embed.add_field(
                        name="Date Joined",
                        value=discord.utils.format_dt(
                            parser.isoparse(getUserProfile["date_joined"]), style="F"
                        ),
                    )
                    embed.set_thumbnail(url=getUserInfo.display_avatar.url)
                    await ctx.respond(embed=embed, ephemeral=True)
            except ItemNotFound:
                embedError = discord.Embed()
                embedError.description = "Sorry, but it seems like you don't have a profile. Make a pull to create one"
                await ctx.respond(embed=embedError, ephemeral=True)


def setup(bot):
    bot.add_cog(GWS(bot))
