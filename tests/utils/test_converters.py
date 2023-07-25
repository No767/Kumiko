import sys
from pathlib import Path

path = Path(__file__).parents[2].joinpath("Bot")
sys.path.append(str(path))
import discord
import discord.ext.test as dpytest
import pytest
import pytest_asyncio
from discord.ext import commands
from Libs.utils import JobName, PinName, PrefixConverter


class PrefixCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="prefix")
    async def prefix(self, ctx, prefix: PrefixConverter):
        await ctx.send(f"{prefix}")


class PinCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="pins")
    async def pins(self, ctx, *, name: PinName):
        await ctx.send(f"{name}")

    @pins.command(name="pins")
    async def pinCommand(self, ctx):
        await ctx.send("hey")

    @pins.command(name="pinner")
    async def pinCommande(self, ctx, *, name: PinName):
        await ctx.send(f"{name}")


class JobCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="jobs")
    async def jobs(self, ctx, *, name: JobName):
        await ctx.send(f"{name}")

    @jobs.command(name="jobs")
    async def jobCommand(self, ctx):
        await ctx.send("hey")


@pytest_asyncio.fixture
async def bot():
    # Setup
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True
    b = commands.Bot(command_prefix=">", intents=intents)
    await b._async_setup_hook()  # setup the loop
    await b.add_cog(PrefixCog(b))
    await b.add_cog(PinCog(b))
    await b.add_cog(JobCog(b))

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


@pytest.mark.asyncio
async def test_invalid_max_pin_name(bot):
    finalStr = ""
    for item, idx in enumerate(range(75)):
        finalStr += f"{item}{idx}"

    with pytest.raises(commands.BadArgument) as e:
        await dpytest.message(f">pins {finalStr}")
    assert (
        e.type == commands.BadArgument
        and "Tag name is a maximum of 100 characters." in str(e.value)
    )


@pytest.mark.asyncio
async def test_same_pin_name(bot):
    with pytest.raises(commands.BadArgument) as e:
        await dpytest.message(f">pins pins")
    assert (
        e.type == commands.BadArgument
        and "This tag name starts with a reserved word." in str(e.value)
    )


@pytest.mark.asyncio
async def test_invalid_max_job_name(bot):
    finalStr = ""
    for item, idx in enumerate(range(75)):
        finalStr += f"{item}{idx}"

    with pytest.raises(commands.BadArgument) as e:
        await dpytest.message(f">jobs {finalStr}")
    assert (
        e.type == commands.BadArgument
        and "Job name is a maximum of 100 characters." in str(e.value)
    )


@pytest.mark.asyncio
async def test_same_job_name(bot):
    with pytest.raises(commands.BadArgument) as e:
        await dpytest.message(f">jobs jobs")
    assert (
        e.type == commands.BadArgument
        and "This Job name starts with a reserved word." in str(e.value)
    )
