import asyncio
from typing import Union

import numpy as np
import uvloop
from kumiko_utils import KumikoCM
from numpy.random import default_rng

from .models import WSData


class KumikoGWSUtils:
    """Kumiko's newly re-written GWS utility class. This class contains the new version of the GWS"""

    def __init__(self, uri: str, models: list) -> None:
        """The constructor for `KumikoGWSUtils`

        Args:
            uri (str): Connection URI
            models (list): _description_
        """
        self.self = self
        self.uri = uri
        self.models = models

    async def getWish(self, star_rank: int, size: int = 1) -> Union[dict, np.ndarray]:
        """Selects all the data based on the star rank from the WS DB, and just randomly picks one out

        Ideally should be randomly picked from the SQL Database, but can cause performance issues on PostgreSQL

        Args:
            star_rank (int): The star rank to choose from
            size (int): The amount of items to sample. Defaults to 1.

        Returns:
            Union[dict, np.ndarray]: A dict containing the data found on the `WSData` model or a numpy array
        """
        async with KumikoCM(uri=self.uri, models=self.models):
            selectedItem = np.array(
                await WSData.filter(star_rank=star_rank).all().values()
            )
            rng = default_rng()
            choice = (
                rng.choice(selectedItem, size=size)[0]
                if size == 1
                else rng.choice(selectedItem, size=size, replace=False)
            )
            return choice

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def determineStarRank(self) -> int:
        """Randomly generates the chance needed and based on chance,
        return which rows based on those stars should be queried

        Returns:
            int: The star rank to use (3-5 inclusive)
        """
        rng = default_rng()
        randomChance = rng.random()

        # Pull rates used here: https://game8.co/games/Genshin-Impact/archives/297443
        if randomChance <= 0.06:
            return 5
        elif randomChance <= 0.051:
            return 4
        elif randomChance <= 94.3:
            return 3

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
