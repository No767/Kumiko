import asyncio
import os
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
from rin_exceptions import ItemNotFound, NoItemsError

load_dotenv()

POSTGRES_PASSWORD = os.getenv("Postgres_Password")
POSTGRES_SERVER_IP = os.getenv("Postgres_Server_IP")
POSTGRES_WS_DATABASE = os.getenv("Postgres_Kumiko_Database")
POSTGRES_USERNAME = os.getenv("Postgres_Username")
POSTGRES_PORT = os.getenv("Postgres_Port")
WS_CONNECTION_URI = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:{POSTGRES_PORT}/{POSTGRES_WS_DATABASE}"

wsUtils = KumikoWSUtils()
wsUserInvUtils = KumikoWSUserInvUtils()
wsUserUtils = KumikoWSUsersUtils()


class PurgeView(discord.ui.View):
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
        checkUserInv = await wsUserInvUtils.getUserInv(
            user_id=interaction.user.id, uri=WS_CONNECTION_URI
        )
        try:
            if len(checkUserInv) == 0:
                raise NoItemsError
            else:
                await wsUserInvUtils.purgeUserInv(
                    user_id=interaction.user.id, uri=WS_CONNECTION_URI
                )
                await interaction.response.send_message(
                    "Everything has been purged from your inventory. This cannot be recovered from.",
                    ephemeral=True,
                )
        except NoItemsError:
            await interaction.response.send_message(
                "It seems like you don't have anything in your GWS inventory. Please try again",
                ephemeral=True,
            )

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


class GWS(commands.Cog):
    """Kumiko's Genshin Wish Simulator (GWS)"""

    def __init__(self, bot):
        self.bot = bot

    gws = SlashCommandGroup(
        "gws", "Commands for Kumiko's Genshin Wish Sim", guild_ids=[970159505390325842]
    )
    gwsWish = gws.create_subgroup(
        "wish", "Wish for some items", guild_ids=[970159505390325842]
    )

    gwsUserInvDelete = gws.create_subgroup(
        "delete", "Deletes some stuff from your inv", guild_ids=[970159505390325842]
    )

    @gwsWish.command(name="one")
    async def gwsWishOne(self, ctx):
        """Allows you to wish for one item"""
        getUserProfile = await wsUserUtils.getUserProfile(
            user_id=ctx.author.id, uri=WS_CONNECTION_URI
        )
        for itemsMain in getUserProfile:
            if int(dict(itemsMain)["pulls"]) % 10 == 0:
                starRank = 4
            elif int(dict(itemsMain)["pulls"]) % 90 == 0:
                starRank = 5
            else:
                starRank = await wsUtils.determineStarRank()
            totalAmount = int(dict(itemsMain)["pulls"]) + 1
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
                    date_obtained=datetime.now().isoformat(),
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
        await ctx.respond(embed=embed)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @gwsWish.command(name="multiple")
    async def gwsWishMultiple(
        self,
        ctx,
        *,
        num_of_wishes: Option(
            int, "The number of wishes to perform", min_value=1, max_value=3
        ),
    ):
        """Allows you to wish for up to 3 items at once"""
        getUserProfile = await wsUserUtils.getUserProfile(
            user_id=ctx.author.id, uri=WS_CONNECTION_URI
        )
        for itemsMain in getUserProfile:
            if int(dict(itemsMain)["pulls"]) % 10 == 0:
                starRank = 4
            elif int(dict(itemsMain)["pulls"]) % 90 == 0:
                starRank = 5
            else:
                starRank = await wsUtils.determineStarRank()
            totalAmount = int(dict(itemsMain)["pulls"]) + num_of_wishes
            await wsUserUtils.updateUserPullCount(
                user_id=ctx.author.id, amount=totalAmount, uri=WS_CONNECTION_URI
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
                        date_obtained=datetime.now().isoformat(),
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
    async def deleteOneUserInv(
        self, ctx, *, name: Option(str, "The name of the item to delete")
    ):
        """Deletes one item from your inventory"""
        checkUserInv = await wsUserInvUtils.getWSItemUserInvOne(
            user_id=ctx.author.id, name=name, uri=WS_CONNECTION_URI
        )
        try:
            if len(checkUserInv) == 0:
                raise ItemNotFound
            else:
                for items in checkUserInv:
                    await wsUserInvUtils.deleteOneUserInv(
                        user_id=ctx.author.id,
                        uuid=dict(items)["item_uuid"],
                        uri=WS_CONNECTION_URI,
                    )
                    await ctx.respond(
                        f"The item {name} has been deleted from your inventory"
                    )
        except ItemNotFound:
            embedError = discord.Embed()
            embedError.description = "Sorry, but it seems like there are no items in your inventory. Please try again"
            await ctx.respond(embed=embedError)

    @gwsUserInvDelete.command(name="all")
    async def purgeUserInv(self, ctx):
        """Deletes all of your items in your GWS inventory"""
        embed = discord.Embed()
        embed.description = "Do you want to purge all of the items from your user inventory? This cannot be undone"
        await ctx.respond(embed=embed, view=PurgeView())

    @gws.command(name="profile")
    async def getUserProfile(self, ctx):
        """Gets your GWS profile"""
        mainRes = await wsUserUtils.getUserProfile(
            user_id=ctx.author.id, uri=WS_CONNECTION_URI
        )
        embed = discord.Embed()
        for items in mainRes:
            getUserInfo = await self.bot.get_or_fetch_user(dict(items)["user_id"])
            embed.title = getUserInfo.name
            embed.add_field(name="Pulls", value=dict(items)["pulls"], inline=True)
            embed.add_field(
                name="Date Joined",
                value=parser.isoparse(dict(items)["date_joined"]).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                inline=True,
            )
            embed.set_thumbnail(url=getUserInfo.display_avatar.url)
        await ctx.respond(embed=embed)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(GWS(bot))
