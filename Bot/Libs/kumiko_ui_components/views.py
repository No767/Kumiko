import asyncio

import discord
import uvloop
from admin_logs_utils import KumikoAdminLogsUtils
from economy_utils import (
    KumikoAuctionHouseUtils,
    KumikoEcoUserUtils,
    KumikoEcoUtils,
    KumikoQuestsUtils,
)
from genshin_wish_sim_utils import KumikoWSUserInvUtils
from rin_exceptions import ItemNotFound, NoItemsError

from .modals import GWSDeleteOneInv, QuestsDeleteOneModal


class ALPurgeDataView(discord.ui.View):
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True

    def __init__(self, uri: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uri = uri
        self.alUtils = KumikoAdminLogsUtils(self.uri)

    @discord.ui.button(
        label="Yes",
        row=0,
        style=discord.ButtonStyle.primary,
        emoji=discord.PartialEmoji.from_str("<:check:314349398811475968>"),
    )
    async def button_callback(self, button, interaction):
        selectAllALGuildData = await self.alUtils.selAllGuildRows(
            guild_id=interaction.guild.id
        )
        try:
            if len(selectAllALGuildData) == 0:
                raise ItemNotFound
            else:
                await self.alUtils.purgeData(guild_id=interaction.guild.id)
                await interaction.response.send_message(
                    "Confirmed. All of the Admin Logs for this server have been purged",
                    ephemeral=True,
                    delete_after=10,
                )
        except ItemNotFound:
            await interaction.response.send_message(
                "It seems like you don't have any to delete from at all...",
                ephemeral=True,
                delete_after=10,
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
            f"The action has been canceled by {interaction.user.name}", ephemeral=True
        )

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


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


class GWSDeleteOneInvView(discord.ui.View):
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
            GWSDeleteOneInv(uri=self.uri, title="Delete a item")
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


class GWSPurgeAllInvView(discord.ui.View):
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True

    def __init__(self, uri: str):
        self.uri = uri
        self.userInv = KumikoWSUserInvUtils()

    @discord.ui.button(
        label="Yes",
        row=0,
        style=discord.ButtonStyle.primary,
        emoji=discord.PartialEmoji.from_str("<:check:314349398811475968>"),
    )
    async def button_callback(self, button, interaction):
        checkUserInv = await self.userInv.getUserInv(
            user_id=interaction.user.id, uri=self.uri
        )
        try:
            if len(checkUserInv) == 0:
                raise NoItemsError
            else:
                await self.userInv.purgeUserInv(
                    user_id=interaction.user.id, uri=self.uri
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
