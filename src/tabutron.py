import discord
import asyncio
import datetime
import logging
from sys import stdout
from os import environ

from discord_logging_handler import DiscordLoggingHandler
from bot_functions import purge_channels

def add_logging_handler(logger, handler, level):
    handler.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def setup_logger(client):
    # Create a default logger. This is sufficient for AWS logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    if 'LAMBDA' in environ:
        # Add logger to #bot-logs in Discord
        add_logging_handler(logger,
                            DiscordLoggingHandler(client, "491405337341984769"),
                            logging.WARN)
    else:
        # Add a console logger for development
        add_logging_handler(logger,
                            logging.StreamHandler(stdout),
                            logging.INFO)
    
    logger.info("Logged in and running ^_^")
    return logger

async def connect():
    client = discord.Client()
    await client.login(environ['DISCORD_API_KEY'])
    asyncio.ensure_future(client.connect())
    await client.wait_until_ready()
    return client

async def main():
    client = await connect()
    logger = setup_logger(client)
    now = datetime.datetime.now()

    await purge_channels(logger, client, now)

    await client.logout()

# Function called by AWS lambda to run the bot
def lambda_handler(event, context):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()

# Call lambda_handler ourselves to run the bot if running locally
if not 'LAMBDA' in environ:
    lambda_handler(None, None)
