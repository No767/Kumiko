import asyncio
import logging
import os

import aiormq
import aiormq.abc
from discord.ext import commands
from dotenv import load_dotenv
from economy_utils import KumikoAuctionHouseUtils

load_dotenv()

RABBITMQ_USER = os.getenv("RabbitMQ_Username_Dev")
RABBITMQ_PASSWORD = os.getenv("RabbitMQ_Password_Dev")
RABBITMQ_SERVER_IP = os.getenv("RabbitMQ_Server_IP_Dev")
POSTGRES_PASSWORD = os.getenv("Postgres_Password_Dev")
POSTGRES_SERVER_IP = os.getenv("Postgres_Server_IP_Dev")
POSTGRES_AH_DATABASE = os.getenv("Postgres_Database_AH_Dev")
POSTGRES_USERNAME = os.getenv("Postgres_Username_Dev")
AH_CONNECTION_URI = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_AH_DATABASE}"

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] | %(asctime)s >> %(message)s",
    datefmt="[%m/%d/%Y] [%I:%M:%S %p %Z]",
)

ahUtils = KumikoAuctionHouseUtils()


async def on_queue_message(message: aiormq.abc.DeliveredMessage) -> None:
    mainMessage = message.body
    decodedMainMessage = mainMessage.decode("utf-8")
    splitMessage = decodedMainMessage.split(":")
    await ahUtils.updateAHItem(
        uuid=splitMessage[0], price=int(splitMessage[1]), uri=AH_CONNECTION_URI
    )

    await message.channel.basic_ack(message.delivery.delivery_tag)


class RabbitMQConsumerProcess:
    def __init__(self):
        self.self = self

    async def mainProc(self):
        """The main process of the RabbitMQ consumer"""
        connection = aiormq.Connection(
            f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_SERVER_IP}/"
        )
        await connection.connect()
        channel = await connection.channel()
        await channel.basic_qos(prefetch_count=1)
        await channel.exchange_declare(exchange="auction_house", exchange_type="fanout")
        declare_ok = await channel.queue_declare(exclusive=True)
        await channel.queue_bind(declare_ok.queue, "auction_house")
        await channel.basic_consume(declare_ok.queue, on_queue_message)


class InitRabbitMQConsumer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_connect(ctx):
        mainProcesses = RabbitMQConsumerProcess()
        task = asyncio.create_task(mainProcesses.mainProc(), name="RabbitMQConsumer")
        background_tasks = set()
        background_tasks.add(await task)
        task.add_done_callback(background_tasks.discard)
        logging.info("Successfully started RabbitMQ consumer")


def setup(bot):
    bot.add_cog(InitRabbitMQConsumer(bot))
