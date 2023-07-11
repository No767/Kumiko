import sys
from pathlib import Path

path = Path(__file__).parents[2].joinpath("Bot")
sys.path.append(str(path))
import discord
import discord.ext.test as dpytest
import pytest
import pytest_asyncio
from discord.ext import commands
from Libs.utils import PrefixConverter


class PrefixCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="prefix")
    async def prefix(self, ctx, prefix: PrefixConverter):
        await ctx.send(f"{prefix}")


@pytest_asyncio.fixture
async def bot():
    # Setup
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True
    b = commands.Bot(command_prefix=">", intents=intents)
    await b._async_setup_hook()  # setup the loop
    await b.add_cog(PrefixCog(b))

    dpytest.configure(b)

    yield b

    # Teardown
    await dpytest.empty_queue()


@pytest.mark.asyncio
async def test_valid_prefix(bot):
    await dpytest.message(">prefix !")
    assert dpytest.verify().message().content("!")


@pytest.mark.asyncio
async def test_invalid_prefix(bot):
    finalStr = ""
    for _ in range(103):
        finalStr += "a"
    with pytest.raises(commands.BadArgument) as e:
        await dpytest.message(f">prefix {finalStr}")
        # assert dpytest.verify().message().content("!")
        assert e.type == commands.BadArgument and "That prefix is too long." in str(
            e.value
        )


@pytest.mark.asyncio
async def test_invalid_ping_prefix(bot):
    user_id = bot.user.id
    finalStr = f"<@{user_id}>"

    with pytest.raises(commands.BadArgument) as e:
        await dpytest.message(f">prefix {finalStr}")
        assert (
            e.type == commands.BadArgument
            and "That is a reserved prefix already in use." in str(e.value)
        )


@pytest.mark.asyncio
async def test_invalid_mention_prefix(bot):
    user_id = bot.user.id
    finalStr = f"<@!{user_id}>"

    with pytest.raises(commands.BadArgument) as e:
        await dpytest.message(f">prefix {finalStr}")
        assert (
            e.type == commands.BadArgument
            and "That is a reserved prefix already in use." in str(e.value)
        )
