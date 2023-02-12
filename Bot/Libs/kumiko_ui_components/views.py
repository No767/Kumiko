import asyncio
from typing import List

import discord
import uvloop
from kumiko_economy import EcoUser
from kumiko_economy_utils import KumikoEcoUserUtils, KumikoEcoUtils, KumikoQuestsUtils
from kumiko_genshin_wish_sim import WSUserInv
from kumiko_utils import KumikoCM
from rin_exceptions import ItemNotFound, NoItemsError

from .modals import QuestsDeleteOneModal


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


class EcoUserCreationView(discord.ui.View):
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @discord.ui.button(
        label="Yes",
        row=0,
        style=discord.ButtonStyle.primary,
        emoji=discord.PartialEmoji.from_str("<:check:314349398811475968>"),
    )
    async def confirm_create_callabck(
        self, button, interaction: discord.Interaction
    ) -> None:
        doesUserExist = await EcoUser.filter(user_id=interaction.user.id).exists()
        if doesUserExist is False:
            await EcoUser(
                user_id=interaction.user.id,
                username=interaction.user.name,
                date_joined=discord.utils.utcnow(),
            ).save()
            for child in self.children:
                child.disabled = True
            return await interaction.response.edit_message(
                embed=discord.Embed(
                    description="Your economy account has been created! Have fun!"
                ),
                view=self,
                delete_after=15.0,
            )
        else:
            for child in self.children:
                child.disabled = True
            return await interaction.response.edit_message(
                embed=discord.Embed(description="You already have an economy account!"),
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


class EcoUserPurgeView(discord.ui.View):
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @discord.ui.button(
        label="Yes",
        row=0,
        style=discord.ButtonStyle.primary,
        emoji=discord.PartialEmoji.from_str("<:check:314349398811475968>"),
    )
    async def confirm_create_callabck(
        self, button, interaction: discord.Interaction
    ) -> None:
        doesUserExist = await EcoUser.filter(user_id=interaction.user.id).exists()
        if doesUserExist is True:
            await EcoUser.filter(user_id=interaction.user.id).delete()
            for child in self.children:
                child.disabled = True
            return await interaction.response.edit_message(
                embed=discord.Embed(
                    description="Your economy account has been deleted. All of your items that is associated with your account has been deleted as well."
                ),
                view=self,
                delete_after=15.0,
            )
        else:
            for child in self.children:
                child.disabled = True
            return await interaction.response.edit_message(
                embed=discord.Embed(
                    description="You don't have an economy account to delete!"
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
