import asyncio
from typing import List

import discord
import uvloop
from kumiko_admin_logs.models import KumikoAdminLogs
from kumiko_economy_utils import (
    KumikoAuctionHouseUtils,
    KumikoEcoUserUtils,
    KumikoEcoUtils,
    KumikoQuestsUtils,
)
from kumiko_genshin_wish_sim import WSUserInv
from kumiko_servers import KumikoServerCacheUtils
from kumiko_utils import KumikoCM
from rin_exceptions import ItemNotFound, NoItemsError

from .modals import QuestsDeleteOneModal


class AHPurgeAllView(discord.ui.View):
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True

    def __init__(self, uri: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uri = uri
        self.userUtils = KumikoEcoUserUtils()
        self.auctionHouseUtils = KumikoAuctionHouseUtils()

    @discord.ui.button(
        label="Yes",
        row=0,
        style=discord.ButtonStyle.primary,
        emoji=discord.PartialEmoji.from_str("<:check:314349398811475968>"),
    )
    async def button_callback(self, button, interaction):
        try:
            getUserInfo = await self.userUtils.selectUserRank(
                interaction.user.id, self.uri
            )
            if len(getUserInfo) == 0:
                raise NoItemsError
            else:
                for items in getUserInfo:
                    if items < 25:
                        await interaction.response.send_message(
                            f"Sorry, but your current rank is {items}. You need at the very least rank 25 or higher to use this command."
                        )
                    else:
                        itemUUIDAuth = await self.auctionHouseUtils.obtainItemUUIDAuth(
                            user_id=interaction.user.id, uri=self.uri
                        )
                        try:
                            if len(itemUUIDAuth) == 0:
                                raise ItemNotFound
                            else:
                                await self.auctionHouseUtils.purgeUserAHItems(
                                    user_id=interaction.user.id, uri=self.uri
                                )
                                await interaction.response.send_message(
                                    "Confirmed. All Auction House Listings have now been completely purged from your account. This is permanent and irreversible.",
                                    ephemeral=True,
                                )
                        except ItemNotFound:
                            await interaction.response.send_message(
                                "It seems like you don't have any to delete from at all...",
                                ephemeral=True,
                            )
        except NoItemsError:
            await interaction.response.send_message(
                "It seems like you don't even have an account to begin with. Go ahead and create one first.",
                ephemeral=True,
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
            "The action has been canceled", ephemeral=True
        )

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class MarketplacePurgeAllView(discord.ui.View):
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True

    def __init__(self, uri: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uri = uri
        self.utilsMain = KumikoEcoUtils()

    @discord.ui.button(
        label="Yes",
        row=0,
        style=discord.ButtonStyle.primary,
        emoji=discord.PartialEmoji.from_str("<:check:314349398811475968>"),
    )
    async def button_callback(self, button, interaction):
        mainChecker = await self.utilsMain.getAllOwnersItems(
            owner=interaction.user.id, uri=self.uri
        )
        try:
            if len(mainChecker) == 0:
                raise NoItemsError
            else:
                for items in mainChecker:
                    await self.utilsMain.purgeOwnersItems(
                        uuid=dict(items)["uuid"],
                        owner=dict(items)["owner"],
                        uri=self.uri,
                    )
                await interaction.response.send_message(
                    "All of your items listed on the marketplace have been deleted",
                    ephemeral=True,
                )
        except NoItemsError:
            await interaction.response.send_message(
                "You don't have any items listed on the marketplace to delete. The transaction has been cancelled.",
                ephemeral=True,
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
            "Welp, you choose not to ig...", ephemeral=True
        )

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class QuestsPurgeAllView(discord.ui.View):
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True

    def __init__(self, user_uri: str, quests_uri: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_uri = user_uri
        self.quests_uri = quests_uri
        self.questsUtil = KumikoQuestsUtils()
        self.userUtils = KumikoEcoUserUtils()

    @discord.ui.button(
        label="Yes",
        row=0,
        style=discord.ButtonStyle.primary,
        emoji=discord.PartialEmoji.from_str("<:check:314349398811475968>"),
    )
    async def button_callback(self, button, interaction: discord.Interaction):
        itemUUIDAuth = await self.questsUtil.getItemUUIDAuth(
            user_id=interaction.user.id,
            uri=self.user_uri,
        )
        userRank = await self.userUtils.selectUserRank(
            user_id=interaction.user.id, uri=self.user_uri
        )
        try:
            if len(itemUUIDAuth) == 0:
                raise ItemNotFound
            else:
                for rank in userRank:
                    if int(rank) < 5:
                        await interaction.response.send_message(
                            f"Sorry, but you can't use the quests feature since you are current rank is {rank}",
                            ephemeral=True,
                        )
                    else:
                        for item in itemUUIDAuth:
                            await self.questsUtil.purgeUserQuests(
                                user_id=interaction.user.id,
                                uuid=item,
                                uri=self.quests_uri,
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
    async def second_button_callback(self, button, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Well glad you choose not to...", ephemeral=True
        )

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class CreateAccountView(discord.ui.View):
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True

    def __init__(self, uri: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uri = uri
        self.utilsUser = KumikoEcoUserUtils()

    @discord.ui.button(
        label="Yes",
        row=0,
        style=discord.ButtonStyle.primary,
        emoji=discord.PartialEmoji.from_str("<:check:314349398811475968>"),
    )
    async def button_callback(self, button, interaction):
        getUser = await self.utilsUser.getFirstUser(
            user_id=interaction.user.id, uri=self.uri
        )
        if getUser is None:
            await self.utilsUser.initUserAcct(
                user_id=interaction.user.id,
                username=interaction.user.name,
                date_joined=discord.utils.utcnow().isoformat(),
                uri=self.uri,
            )
            await interaction.response.send_message(
                "Confirmed. Now you have access to the marketplace!", ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "Looks like you already have an account. You can't sign up for extras",
                ephemeral=True,
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
            f"The operation has been canceled by the user {interaction.user.name}",
            ephemeral=True,
        )

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class PurgeAccountView(discord.ui.View):
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True

    def __init__(self, uri: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uri = uri
        self.utilsUser = KumikoEcoUserUtils()

    @discord.ui.button(
        label="Yes",
        row=0,
        style=discord.ButtonStyle.primary,
        emoji=discord.PartialEmoji.from_str("<:check:314349398811475968>"),
    )
    async def button_callback(self, button, interaction):
        getUser = await self.utilsUser.getFirstUser(
            user_id=interaction.user.id, uri=self.uri
        )
        if getUser is None:
            await interaction.response.send_message(
                "You probably have already deleted the account...", ephemeral=True
            )
        else:
            await self.utilsUser.deleteUser(user_id=interaction.user.id, uri=self.uri)
            await interaction.response.send_message(
                "Confirmed. Your have permanently deleted your account.", ephemeral=True
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
            f"The action has been cancelled by the user {interaction.user.name}",
            ephemeral=True,
        )

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class QuestsDeleteOneConfirmView(discord.ui.View):
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True

    def __init__(self, uri: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uri = uri

    @discord.ui.button(
        label="Yes",
        row=0,
        style=discord.ButtonStyle.primary,
        emoji=discord.PartialEmoji.from_str("<:check:314349398811475968>"),
    )
    async def button_callback(self, button, interaction):
        await interaction.response.send_modal(
            QuestsDeleteOneModal(uri=self.uri, title="Delete a quest")
        )

    @discord.ui.button(
        label="No",
        row=0,
        style=discord.ButtonStyle.primary,
        emoji=discord.PartialEmoji.from_str("<:xmark:314349398824058880>"),
    )
    async def second_button_callback(self, button, interaction):
        await interaction.response.send_message(
            f"The action has been cancelled by the user {interaction.user.name}",
            ephemeral=True,
        )

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class GWSPurgeInvView(discord.ui.View):
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True

    def __init__(self, uri: str, models: List, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.uri = uri
        self.models = models

    @discord.ui.button(
        label="Yes",
        row=0,
        style=discord.ButtonStyle.primary,
        emoji=discord.PartialEmoji.from_str("<:check:314349398811475968>"),
    )
    async def button_callback(self, button, interaction: discord.Interaction):
        async with KumikoCM(uri=self.uri, models=self.models):
            invExist = await WSUserInv.filter(user_id=interaction.user.id).exists()
            if invExist is False:
                for child in self.children:
                    child.disabled = True
                await interaction.response.edit_message(
                    embed=discord.Embed(
                        description="It seems like you don't have anything in your GWS inventory. Please try again"
                    ),
                    view=self,
                    delete_after=15.0,
                )
            else:
                await WSUserInv.filter(user_id=interaction.user.id).delete()
                for child in self.children:
                    child.disabled = True
                await interaction.response.edit_message(
                    embed=discord.Embed(
                        description="Everything has been purged from your inventory. This cannot be recovered from."
                    ),
                    view=self,
                    delete_after=15.0,
                )

    @discord.ui.button(
        label="No",
        row=0,
        style=discord.ButtonStyle.primary,
        emoji=discord.PartialEmoji.from_str("<:xmark:314349398824058880>"),
    )
    async def second_button_callback(self, button, interaction: discord.Interaction):
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(
            embed=discord.Embed(
                description=f"This action has been canceled by {interaction.user.name}"
            ),
            view=self,
            delete_after=15.0,
        )


class AdminLogsPurgeAllView(discord.ui.View):
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True

    def __init__(
        self,
        uri: str,
        models: List,
        redis_host: str,
        redis_port: int,
        command_name: str,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.uri = uri
        self.models = models
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.command_name = command_name
        self.cache = KumikoServerCacheUtils(
            uri=self.uri,
            models=self.models,
            redis_host=self.redis_host,
            redis_port=self.redis_port,
        )

    @discord.ui.button(
        label="Yes",
        row=0,
        style=discord.ButtonStyle.primary,
        emoji=discord.PartialEmoji.from_str("<:check:314349398811475968>"),
    )
    async def confirm_purge_callback(
        self, button, interaction: discord.Interaction
    ) -> None:
        async with KumikoCM(uri=self.uri, models=self.models):
            adminLogsExists = await KumikoAdminLogs.filter(
                guild_id=interaction.guild.id
            ).exists()
            serverData = await self.cache.cacheServer(
                guild_id=interaction.guild.id, command_name=self.command_name
            )
            if adminLogsExists is False or int(serverData["admin_logs"]) == 0:
                for child in self.children:
                    child.disabled = True
                return await interaction.response.edit_message(
                    embed=discord.Embed(
                        description="It seems like there could be no admin logs found. This is usually due to Admin Logs not being enabled"
                    ),
                    view=self,
                    delete_after=15.0,
                )
            else:
                await KumikoAdminLogs.filter(guild_id=interaction.guild.id).delete()
                for child in self.children:
                    child.disabled = True
                return await interaction.response.edit_message(
                    embed=discord.Embed(
                        description="All of the admin logs for this server has been completely wiped."
                    ),
                    view=self,
                    delete_after=15.0,
                )

    @discord.ui.button(
        label="No",
        row=0,
        style=discord.ButtonStyle.primary,
        emoji=discord.PartialEmoji.from_str("<:xmark:314349398824058880>"),
    )
    async def cancel_action_callback(
        self, button, interaction: discord.Interaction
    ) -> None:
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(
            embed=discord.Embed(
                description=f"This action has been canceled by {interaction.user.name}"
            ),
            view=self,
            delete_after=15.0,
        )
