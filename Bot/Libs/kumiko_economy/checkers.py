import logging

from dateutil import parser
from discord.utils import utcnow
from kumiko_economy import KumikoAuctionHouseUtils, KumikoQuestsUtils
from rin_exceptions import ItemNotFound, NoItemsError

questUtils = KumikoQuestsUtils()
ahUtils = KumikoAuctionHouseUtils()


async def QuestsChecker(uri: str) -> None:
    """Checks quests every hour and deactivates them if they're expired"""
    activeQuests = await questUtils.getAllActiveQuests(active=True, uri=uri)
    try:
        if len(activeQuests) == 0:
            raise NoItemsError
        else:
            for questItem in activeQuests:
                today = utcnow()
                parsedDate = parser.isoparse(dict(questItem)["end_datetime"])
                if parsedDate < today:
                    await questUtils.setQuestActiveStatus(
                        uuid=dict(questItem)["uuid"],
                        active=False,
                        uri=uri,
                    )
                elif parsedDate == today:
                    await questUtils.setQuestActiveStatus(
                        uuid=dict(questItem)["uuid"],
                        active=False,
                        uri=uri,
                    )
    except NoItemsError:
        logging.warning(
            "No quests found to be active in the DB. Continuing to check for more"
        )


async def AHChecker(uri: str) -> None:
    """Checks every hour for new AH items

    Args:
        uri (str): Connection URI
    """
    mainRes = await ahUtils.obtainAHItemPassed(passed=False, uri=uri)
    try:
        if len(mainRes) == 0:
            raise ItemNotFound
        else:
            for item in mainRes:
                mainItem = dict(item)
                today = utcnow()
                parsedDate = parser.isoparse(dict(mainItem)["date_added"])
                if parsedDate < today:
                    await ahUtils.setAHItemBoolean(
                        uuid=dict(mainItem)["uuid"],
                        passed=True,
                        uri=uri,
                    )
                elif parsedDate == today:
                    await ahUtils.setAHItemBoolean(
                        uuid=dict(mainItem)["uuid"],
                        passed=True,
                        uri=uri,
                    )
    except ItemNotFound:
        logging.warning(
            "No items found in the AH database. Continuing to check for more"
        )
