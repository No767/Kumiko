import glob
import os

import discord
import discord.ext.commands as commands
import discord.ext.test as dpytest
import pytest_asyncio
from cogs.mod import ModCog


@pytest_asyncio.fixture
async def bot():
    # Setup
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True
    b = commands.Bot(command_prefix="!", intents=intents)
    await b._async_setup_hook()
    dpytest.configure(b)
    await b.add_cog(ModCog(b))

    yield b

    # Teardown
    await dpytest.empty_queue()  # empty the global message queue as test teardown


def pytest_sessionfinish(session, exitstatus):
    """Code to execute after all tests."""

    # dat files are created when using attachements
    print("\n-------------------------\nClean dpytest_*.dat files")
    file_list = glob.glob("./dpytest_*.dat")
    for file_path in file_list:
        try:
            os.remove(file_path)
        except Exception:
            print("Error while deleting file : ", file_path)
