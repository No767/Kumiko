import asyncio
import uuid
from typing import List

import discord
import uvloop
from dateutil import parser
from kumiko_economy import EcoMarketplace, EcoUser
from kumiko_economy_utils import (
    KumikoAuctionHouseUtils,
    KumikoEcoUserUtils,
    KumikoEcoUtils,
    KumikoQuestsUtils,
    KumikoUserInvUtils,
)
from kumiko_genshin_wish_sim import KumikoGWSCacheUtils, WSUserInv
from kumiko_utils import KumikoCM
from rin_exceptions import ItemNotFound


class QuestsDeleteOneModal(discord.ui.Modal):
    def __init__(self, uri: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.uri = uri
        self.questsUtil = KumikoQuestsUtils()
        self.userUtils = KumikoEcoUserUtils()

        self.add_item(
            discord.ui.InputText(
                label="Quest name",
                style=discord.InputTextStyle.short,
                min_length=1,
                required=True,
                placeholder="Type in the quest name to delete",
            )
        )

    async def callback(self, interaction: discord.Interaction):
        mainRes = await self.questsUtil.getUserQuestOne(
            user_id=interaction.user.id, name=self.children[0].value, uri=self.uri
        )
        userRank = await self.userUtils.selectUserRank(
            user_id=interaction.user.id, uri=self.uri
        )
        try:
            if len(userRank) == 0:
                raise ItemNotFound
            else:
                for items in userRank:
                    if int(items) < 5:
                        return await interaction.response.send_message(
                            f"Sorry, but you can't use the quests feature since you are current rank is {items}",
                            ephemeral=True,
                        )
                    elif mainRes is None:
                        return await interaction.response.send_message(
                            f"Sorry, but the quest {self.children[0].value} could not be found. Please try again",
                            ephemeral=True,
                        )
                    else:
                        await self.questsUtil.deleteOneQuest(
                            user_id=interaction.user.id,
                            uuid=dict(mainRes)["uuid"],
                            uri=self.uri,
                        )
                        return await interaction.response.send_message(
                            f"Quest {self.children[0].value} has been deleted",
                            ephemeral=True,
                        )
        except ItemNotFound:
            return await interaction.response.send_message(
                "It seems like you either don't have an account yet, or the the quest you requested is not found. Please try again",
                ephemeral=True,
            )

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class QuestsCreateModal(discord.ui.Modal):
    def __init__(self, uri: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.uri = uri
        self.questsUtil = KumikoQuestsUtils()
        self.userUtils = KumikoEcoUserUtils()

        self.add_item(
            discord.ui.InputText(
                label="Name",
                style=discord.InputTextStyle.short,
                min_length=1,
                required=True,
                placeholder="Type in the quest name to create",
            )
        )
        self.add_item(
            discord.ui.InputText(
                label="Description",
                style=discord.InputTextStyle.long,
                min_length=1,
                required=True,
                placeholder="Type in the quest description",
            )
        )
        self.add_item(
            discord.ui.InputText(
                label="Reward",
                style=discord.InputTextStyle.short,
                min_length=1,
                required=True,
                placeholder="Type in the number of petals to reward",
            )
        )
        self.add_item(
            discord.ui.InputText(
                label="End Date",
                style=discord.InputTextStyle.short,
                min_length=1,
                required=True,
                placeholder="Type in the end date of the quest",
            )
        )
        self.add_item(
            discord.ui.InputText(
                label="End Time",
                style=discord.InputTextStyle.short,
                min_length=1,
                required=True,
                placeholder="Type in the end time of the quest",
            )
        )

    async def callback(self, interaction: discord.Interaction):
        getUser = await self.userUtils.getFirstUser(
            user_id=interaction.user.id, uri=self.uri
        )
        if getUser is None:
            await interaction.response.send_message(
                "Probably should create an account first...", ephemeral=True
            )
        elif int(dict(getUser)["rank"]) < 5:
            await interaction.response.send_message(
                f"Sorry, but you can't use the quests feature since you are current rank is {dict(getUser)['rank']}",
                ephemeral=True,
            )
        else:
            questUUIDItem = str(uuid.uuid4())
            dateCreated = discord.utils.utcnow().isoformat()
            endDateFormatted = parser.parse(
                f"{self.children[3].value} {self.children[4].value}"
            ).isoformat()
            totalUserPetals = int(dict(getUser)["lavender_petals"]) - int(
                self.children[2].value
            )
            await self.userUtils.updateUserLavenderPetals(
                user_id=interaction.user.id,
                lavender_petals=totalUserPetals,
                uri=self.uri,
            )
            await self.questsUtil.createQuests(
                uuid=questUUIDItem,
                creator=interaction.user.id,
                claimed_by=None,
                date_created=dateCreated,
                end_datetime=endDateFormatted,
                name=self.children[0].value,
                description=self.children[1].value,
                reward=int(self.children[2].value),
                active=True,
                claimed=False,
                uri=self.uri,
            )
            await interaction.response.send_message(
                f"Quest {self.children[0].value} has been created", ephemeral=True
            )

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class QuestsUpdateTimeModal(discord.ui.Modal):
    def __init__(self, uri: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.uri = uri
        self.questsUtil = KumikoQuestsUtils()
        self.userUtils = KumikoEcoUserUtils()

        self.add_item(
            discord.ui.InputText(
                label="Name",
                style=discord.InputTextStyle.short,
                min_length=1,
                required=True,
                placeholder="Type in the quest name to search for",
            )
        )
        self.add_item(
            discord.ui.InputText(
                label="End Date",
                style=discord.InputTextStyle.short,
                min_length=1,
                required=True,
                placeholder="Type in the new end date of the quest",
            )
        )
        self.add_item(
            discord.ui.InputText(
                label="End Time",
                style=discord.InputTextStyle.short,
                min_length=1,
                required=True,
                placeholder="Type in the new end time of the quest",
            )
        )

    async def callback(self, interaction: discord.Interaction):
        mainQuest = await self.questsUtil.getQuestViaName(
            name=self.children[0].value, uri=self.uri
        )
        mainUserData = await self.userUtils.obtainUserData(
            user_id=interaction.user.id, uri=self.uri
        )
        try:
            if len(mainQuest) == 0 or len(mainUserData) == 0:
                raise ItemNotFound
            else:
                fullDateTime = parser.parse(
                    f"{self.children[1].value} {self.children[2].value}"
                ).isoformat()
                for userData in mainUserData:
                    currentUserRank = dict(userData)["rank"]
                if currentUserRank < 5:
                    await interaction.response.send_message(
                        f"Sorry, but you can't use the quests feature since you are current rank is {currentUserRank}"
                    )
                else:
                    for items in mainQuest:
                        await self.questsUtil.updateDatetimeQuest(
                            uuid=dict(items)["uuid"],
                            new_end_datetime=fullDateTime,
                            uri=self.uri,
                        )
                        await interaction.response.send_message(
                            f"Quest {self.children[0].value} has been updated",
                            ephemeral=True,
                        )
        except ItemNotFound:
            await interaction.response.send_message(
                "It seems like there no quests with that name (or you haven't created an account yet). Please try again"
            )

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class MarketplaceAddItem(discord.ui.Modal):
    def __init__(self, mongo_uri: str, postgres_uri: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.mongoURI = mongo_uri
        self.postgresURI = postgres_uri
        self.user = KumikoEcoUserUtils()
        self.mUtils = KumikoEcoUtils()

        self.add_item(
            discord.ui.InputText(
                label="Name",
                style=discord.InputTextStyle.short,
                min_length=1,
                max_length=255,
                required=True,
                placeholder="Type in the item name here",
            )
        )
        self.add_item(
            discord.ui.InputText(
                label="Description",
                style=discord.InputTextStyle.long,
                min_length=1,
                required=True,
                placeholder="Type in the item description here",
            )
        )
        self.add_item(
            discord.ui.InputText(
                label="Amount",
                style=discord.InputTextStyle.short,
                min_length=1,
                required=True,
                placeholder="Type in how much you are willing to sell here",
            )
        )
        self.add_item(
            discord.ui.InputText(
                label="Price",
                style=discord.InputTextStyle.short,
                min_length=1,
                required=True,
                placeholder="Type in the price of the item here",
            )
        )

    async def callback(self, interaction: discord.Interaction):
        getUserData = await self.user.getFirstUser(
            user_id=interaction.user.id, uri=self.postgresURI
        )
        try:
            if getUserData is None:
                raise ItemNotFound
            else:
                finalBal = int(dict(getUserData)["lavender_petals"]) - 10
                await self.user.updateUserLavenderPetals(
                    user_id=interaction.user.id,
                    lavender_petals=finalBal,
                    uri=self.postgresURI,
                )
                await self.mUtils.ins(
                    uuid=str(uuid.uuid4()),
                    date_added=discord.utils.utcnow().isoformat(),
                    owner=interaction.user.id,
                    owner_name=interaction.user.name,
                    uri=self.mongoURI,
                    name=self.children[0].value,
                    description=self.children[1].value,
                    amount=self.children[2].value,
                    price=self.children[3].value,
                    updatedPrice=False,
                )
                await interaction.response.send_message(
                    f"The item {self.children[0].value} has been added to the marketplace",
                    ephemeral=True,
                )
        except ItemNotFound:
            embed = discord.Embed()
            embed.description = "It seems like your account was not found. Please initialize your account first"
            await interaction.response.send_message(embed=embed, ephemeral=True)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class MarketplaceDeleteOneItem(discord.ui.Modal):
    def __init__(self, mongo_uri: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.mongoURI = mongo_uri
        self.mUtils = KumikoEcoUtils()

        self.add_item(
            discord.ui.InputText(
                label="Name",
                style=discord.InputTextStyle.short,
                min_length=1,
                max_length=255,
                required=True,
                placeholder="Type in the item name here to delete",
            )
        )

    async def callback(self, interaction: discord.Interaction):
        getUserItem = await self.mUtils.obtainUserItem(
            name=self.children[0].value, user_id=interaction.user.id, uri=self.mongoURI
        )
        try:
            if getUserItem is None:
                raise ItemNotFound
            else:
                await getUserItem.delete()
                await interaction.response.send_message(
                    f"The item {self.children[0].value} has been deleted from the marketplace",
                    ephemeral=True,
                )
        except ItemNotFound:
            embed = discord.Embed()
            embed.description = f"It seems like there is no item called {self.children[0].value} in the marketplace. Please try again"
            await interaction.response.send_message(embed=embed, ephemeral=True)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class MarketplaceUpdateAmount(discord.ui.Modal):
    def __init__(self, mongo_uri: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.mongoURI = mongo_uri
        self.mUtils = KumikoEcoUtils()

        self.add_item(
            discord.ui.InputText(
                label="Name",
                style=discord.InputTextStyle.short,
                min_length=1,
                max_length=255,
                required=True,
                placeholder="Type in the item name here to restorck",
            )
        )
        self.add_item(
            discord.ui.InputText(
                label="Amount",
                style=discord.InputTextStyle.short,
                min_length=1,
                max_length=255,
                required=True,
                placeholder="Type in the amount of the item here to restock",
            )
        )

    async def callback(self, interaction: discord.Interaction):
        getUserItem = await self.mUtils.obtainUserItem(
            name=self.children[0].value, user_id=interaction.user.id, uri=self.mongoURI
        )
        try:
            if getUserItem is None:
                raise ItemNotFound
            else:
                totalAmount = int(dict(getUserItem)["amount"]) + int(
                    self.children[1].value
                )
                getUserItem.amount = totalAmount
                await getUserItem.save()
                await interaction.response.send_message(
                    f"Updated {self.children[0].value}'s amount to {totalAmount}",
                    ephemeral=True,
                )
        except ItemNotFound:
            embedError = discord.Embed()
            embedError.description = "Sorry, it seems like the item you are trying to update does not exist in the Marketplace. Please try again."
            await interaction.response.send_message(embed=embedError, ephemeral=True)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class MarketplaceUpdateItemPrice(discord.ui.Modal):
    def __init__(self, mongo_uri: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.mongoURI = mongo_uri
        self.mUtils = KumikoEcoUtils()

        self.add_item(
            discord.ui.InputText(
                label="Name",
                style=discord.InputTextStyle.short,
                min_length=1,
                max_length=255,
                required=True,
                placeholder="Type in the item name here to restorck",
            )
        )
        self.add_item(
            discord.ui.InputText(
                label="Price",
                style=discord.InputTextStyle.short,
                min_length=1,
                max_length=255,
                required=True,
                placeholder="Type in the new price of the item",
            )
        )

    async def callback(self, interaction: discord.Interaction):
        getUserItem = await self.mUtils.obtainUserItem(
            name=self.children[0].value, user_id=interaction.user.id, uri=self.mongoURI
        )
        try:
            if getUserItem is None:
                raise ItemNotFound
            elif dict(getUserItem)["updated_price"] is True:
                await interaction.response.send_message(
                    f"Sorry, you cannot update the price of {self.children[0].value} anymore",
                    ephemeral=True,
                )
            else:
                getUserItem.price = int(self.children[1].value)
                getUserItem.updated_price = True
                await getUserItem.save()
                await interaction.response.send_message(
                    f"Updated {self.children[0].value}'s price {int(self.children[1].value)}",
                    ephemeral=True,
                )
        except ItemNotFound:
            embedError = discord.Embed()
            embedError.description = "Sorry, it seems like the item you are trying to update does not exist in the Marketplace. Please try again."
            await interaction.response.send_message(embed=embedError, ephemeral=True)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class AHCreateItemModal(discord.ui.Modal):
    def __init__(
        self, uri: str, redis_host: str, redis_port: int, *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.uri = uri
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.ahUtils = KumikoAuctionHouseUtils()
        self.userUtils = KumikoEcoUserUtils()

        self.add_item(
            discord.ui.InputText(
                label="Name",
                style=discord.InputTextStyle.short,
                min_length=1,
                max_length=255,
                required=True,
                placeholder="Type in the item name here to create",
            )
        )
        self.add_item(
            discord.ui.InputText(
                label="Description",
                style=discord.InputTextStyle.short,
                min_length=1,
                max_length=255,
                required=True,
                placeholder="What will the description be ?",
            )
        )
        self.add_item(
            discord.ui.InputText(
                label="Price",
                style=discord.InputTextStyle.short,
                min_length=1,
                max_length=255,
                required=True,
                placeholder="Type in the new price of the item",
            )
        )

    async def callback(self, interaction: discord.Interaction):
        try:
            getUserInfo = await self.userUtils.getFirstUser(
                user_id=interaction.user.id, uri=self.uri
            )
            if getUserInfo is None:
                raise ItemNotFound
            else:
                userInfo = dict(getUserInfo)
                if userInfo["rank"] < 25:
                    await interaction.response.send_message(
                        f"Sorry, you need to be at least rank 25 to create an item in the Auction House. Your rank is {userInfo['rank']}",
                        ephemeral=True,
                    )
                elif userInfo["rank"] > 25 and userInfo["lavender_petals"] < 1500:
                    await interaction.response.send_message(
                        "it seems like you don't have enough money to list. You need at the very least 1500 Petals to list",
                        ephemeral=True,
                    )
                elif userInfo["rank"] > 25 and userInfo["lavender_petals"] >= 1500:
                    ahItemUUID = str(uuid.uuid4())
                    await self.ahUtils.addAuctionHouseItem(
                        uuid=ahItemUUID,
                        user_id=interaction.user.id,
                        name=self.children[0].value,
                        description=self.children[1].value,
                        date_added=discord.utils.utcnow().isoformat(),
                        price=int(self.children[2].value),
                        passed=False,
                        uri=self.uri,
                    )
                    await self.ahUtils.setItemKey(
                        key=ahItemUUID,
                        value=self.children[2].value,
                        db=0,
                        ttl=86400,
                        redis_server_ip=self.redis_host,
                        redis_port=self.redis_port,
                    )
                    await interaction.response.send_message(
                        "Successfully added the item to the auction house",
                        ephemeral=True,
                    )
        except ItemNotFound:
            await interaction.response.send_message(
                "It seems like you don't have an account to begin with. Please go ahead and create one.",
                ephemeral=True,
            )

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class AHDeleteItemModal(discord.ui.Modal):
    def __init__(self, uri: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.uri = uri
        self.userUtils = KumikoEcoUserUtils()
        self.ahUtils = KumikoAuctionHouseUtils()
        self.add_item(
            discord.ui.InputText(
                label="Name",
                style=discord.InputTextStyle.short,
                min_length=1,
                max_length=255,
                required=True,
                placeholder="Type in the item name here to delete",
            )
        )

    async def callback(self, interaction: discord.Interaction):
        try:
            getUser = await self.userUtils.getFirstUser(
                user_id=interaction.user.id, uri=self.uri
            )
            if getUser is None:
                raise ItemNotFound
            else:
                if dict(getUser)["rank"] < 25:
                    await interaction.response.send_message(
                        f"Sorry, you need to be at least rank 25 to delete an item in the Auction House. Your rank is {dict(getUser)['rank']}",
                        ephemeral=True,
                    )
                else:
                    getUserItem = await self.ahUtils.selectUserItemNameFirst(
                        user_id=interaction.user.id,
                        name=self.children[0].value,
                        uri=self.uri,
                    )
                    if getUserItem is None:
                        await interaction.response.send_message(
                            f"The item requested ({self.children[0].value}) could not be found. Please try again",
                            ephemeral=True,
                        )
                    else:
                        await self.ahUtils.deleteUserAHItem(
                            user_id=interaction.user.id,
                            uuid=dict(getUserItem)["uuid"],
                            uri=self.uri,
                        )
                        await interaction.response.send_message(
                            f"Successfully deleted {self.children[0].value} from the Auction House",
                            ephemeral=True,
                        )
        except ItemNotFound:
            await interaction.response.send_message(
                "It seems like you don't have an account to begin with. Please go ahead and create one.",
                ephemeral=True,
            )

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class MarketplacePurchaseItemModal(discord.ui.Modal):
    def __init__(self, mongo_uri: str, postgres_uri: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.mongo_uri = mongo_uri
        self.postgres_uri = postgres_uri
        self.mUtils = KumikoEcoUtils()
        self.userUtils = KumikoEcoUserUtils()
        self.userInvUtils = KumikoUserInvUtils()
        self.add_item(
            discord.ui.InputText(
                label="Item Name",
                style=discord.InputTextStyle.short,
                min_length=1,
                max_length=255,
                required=True,
                placeholder="Type in the item name here to purchase",
            )
        )
        self.add_item(
            discord.ui.InputText(
                label="Amount",
                style=discord.InputTextStyle.short,
                min_length=1,
                max_length=255,
                required=True,
                placeholder="Type in the item amount to purchase",
            )
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        getUserInv = await self.userInvUtils.findItem(
            user_id=interaction.user.id,
            item_name=self.children[0].value,
            uri=self.postgres_uri,
        )
        getUser = await self.userUtils.getFirstUser(
            user_id=interaction.user.id, uri=self.postgres_uri
        )
        getRequestedItem = await self.mUtils.getRequestedPurchaseItem(
            name=self.children[0].value, uri=self.mongo_uri
        )

        if getRequestedItem is None:
            await interaction.followup.send(
                f"The item {self.children[0].value} could not be found. Please try again",
                ephemeral=True,
            )
        elif getUser is None:
            await interaction.followup.send(
                "It seems like you forgot to create an account first. Please do that first",
                ephemeral=True,
            )
        else:
            stock = dict(getRequestedItem)["amount"]
            requestedAmount = int(self.children[1].value)
            totalRemaining = stock - requestedAmount
            totalToDeduct = int(dict(getUser)["lavender_petals"]) - int(
                dict(getRequestedItem)["price"]
            )

            if stock <= 0:
                await interaction.followup.send(
                    f"The item {self.children[0].value} is out of stock. Please try again later",
                    ephemeral=True,
                )
            elif requestedAmount > stock:
                await interaction.followup.send(
                    f"The amount requested ({requestedAmount}) is more than the stock ({stock}). Please try again",
                    ephemeral=True,
                )
            elif requestedAmount == stock:
                await self.userUtils.updateUserLavenderPetals(
                    user_id=interaction.user.id,
                    lavender_petals=totalToDeduct,
                    uri=self.postgres_uri,
                )
                purchaseItem = await self.mUtils.purchaseItem(
                    user_inv=getUserInv,
                    requested_item=getRequestedItem,
                    current_stock=totalRemaining if totalRemaining > 0 else 0,
                    requested_amount=self.children[1].value,
                    user_id=interaction.user.id,
                    mongo_uri=self.mongo_uri,
                    postgres_uri=self.postgres_uri,
                )
                await interaction.followup.send(purchaseItem, ephemeral=True)
            elif requestedAmount < stock:
                await self.userUtils.updateUserLavenderPetals(
                    user_id=interaction.user.id,
                    lavender_petals=totalToDeduct,
                    uri=self.postgres_uri,
                )
                purchaseItem = await self.mUtils.purchaseItem(
                    user_inv=getUserInv,
                    requested_item=getRequestedItem,
                    current_stock=totalRemaining if totalRemaining > 0 else 0,
                    requested_amount=self.children[1].value,
                    user_id=interaction.user.id,
                    mongo_uri=self.mongo_uri,
                    postgres_uri=self.postgres_uri,
                )
                await interaction.followup.send(purchaseItem, ephemeral=True)
            else:
                await interaction.followup.send(
                    "The transaction was not successful. Please try again",
                    ephemeral=True,
                )

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class GWSDeleteOneUserInvItemModal(discord.ui.Modal):
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
        self.cache = KumikoGWSCacheUtils(
            uri=self.uri,
            models=self.models,
            redis_host=self.redis_host,
            redis_port=self.redis_port,
        )
        self.add_item(
            discord.ui.InputText(
                label="Name",
                placeholder="Type in the item name to delete",
                min_length=1,
                max_length=255,
                required=True,
                style=discord.InputTextStyle.short,
            )
        )
        self.add_item(
            discord.ui.InputText(
                label="Amount",
                placeholder="Type in the item amount to delete",
                min_length=1,
                max_length=255,
                required=True,
                style=discord.InputTextStyle.short,
            )
        )

    async def callback(self, interaction: discord.Interaction):
        async with KumikoCM(uri=self.uri, models=self.models):
            userInvItem = await self.cache.cacheUserInvItem(
                user_id=interaction.user.id,
                name=self.children[0].value,
                command_name=self.command_name,
            )
            if userInvItem is None:
                return await interaction.response.send_message(
                    f"The item ({self.children[0].value}) could not be found. Please try again",
                    ephemeral=True,
                )
            elif int(self.children[1].value) > userInvItem["amount"]:
                return await interaction.response.send_message(
                    f"The amount requested ({self.children[1].value}) is more than the amount you have ({userInvItem['amount']}). Please try again",
                    ephemeral=True,
                )
            else:
                await WSUserInv.filter(
                    user_id=interaction.user.id, name=userInvItem["name"]
                ).update(amount=userInvItem["amount"] - int(self.children[1].value))
                return await interaction.response.send_message(
                    f"Deleted {self.children[1].value} {self.children[0].value}(s) from your inventory",
                    ephemeral=True,
                )


class EcoMarketplaceListItemModal(discord.ui.Modal):
    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.add_item(
            discord.ui.InputText(
                style=discord.InputTextStyle.short,
                label="Item Name",
                min_length=3,
                max_length=255,
                required=True,
                row=0,
            )
        )
        self.add_item(
            discord.ui.InputText(
                style=discord.InputTextStyle.short,
                label="Price",
                min_length=1,
                max_length=20,
                required=True,
                row=2,
            )
        )
        self.add_item(
            discord.ui.InputText(
                style=discord.InputTextStyle.long,
                label="Description",
                min_length=1,
                max_length=512,
                required=True,
                row=1,
            )
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        # Wish i could use the cache here... but whatever
        currUser = await EcoUser.filter(user_id=interaction.user.id).get_or_none()
        if currUser is None:
            await interaction.response.send_message(
                "You do not have an account. Please create one using the /eco-user init command",
                ephemeral=True,
            )
        else:
            await EcoMarketplace(
                owner=currUser,
                owner_name=interaction.user.name,
                name=self.children[0].value,
                description=self.children[2].value,
                price=self.children[1].value,
                amount=1,
            ).save()
            await interaction.response.send_message(
                f"Added {self.children[0].value} to the marketplace", ephemeral=True
            )
