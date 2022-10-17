import asyncio
import uuid

import discord
import uvloop
from dateutil import parser
from economy_utils import KumikoEcoUserUtils, KumikoQuestsUtils
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
                    elif mainRes is None or len(mainRes) == 0:
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
