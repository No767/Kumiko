import asyncio
import os

import discord
import motor.motor_asyncio
import uvloop
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

Password = os.getenv("MongoDB_Password")
Username = os.getenv("MongoDB_Username")
Server_IP = os.getenv("MongoDB_Server_IP")
    
# This is going to get replaced soon...
