import sys
from pathlib import Path

path = Path(__file__).parents[2].joinpath("Bot")
sys.path.append(str(path))

import discord.ext.test as dpytest
import pytest
from conftest import bot  # type: ignore
from discord.ext import commands

new_bot = bot


@pytest.mark.asyncio
async def test_invalid_convert(bot):
    with pytest.raises(commands.BadArgument) as e:
        await dpytest.message("!modconvert WHATTHEHELLISWRONGWITHYOU")
        assert (
            e.type == commands.BadArgument
            and "Cannot parse datetime argument" in str(e.value)
        )


@pytest.mark.asyncio
async def test_too_much_convert(bot):
    with pytest.raises(commands.BadArgument) as e:
        await dpytest.message("!modconvert Dec 1 3033")
        assert (
            e.type == commands.BadArgument
            and "Timeout cannot be more than 28 days from the given date."
            in str(e.value)
        )


@pytest.mark.asyncio
async def test_convert(bot):
    await dpytest.message("!modconvert 24 hours later UTC")
    assert dpytest.verify().message().contains()

    await dpytest.message("!modconvert 2 hours PST")
    assert dpytest.verify().message().contains()
