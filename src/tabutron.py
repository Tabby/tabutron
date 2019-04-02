import discord
import asyncio
import datetime
import logging
from sys import stdout
from os import environ

from bot_functions import purge_channels

# Create a default logger. This is sufficient for AWS logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

if not 'LAMBDA' in environ:
    # Add a console logger for development
    handler = logging.StreamHandler(stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

client = discord.Client()
token = environ['DISCORD_API_KEY']

output_channel_id = "491405337341984769"

async def main():
    await client.login(token)
    asyncio.ensure_future(client.connect())
    await client.wait_until_ready()

    out_channel = client.get_channel(output_channel_id)
    now = datetime.datetime.now()
    logger.info("Logged in and running ^_^")

    await purge_channels(logger, client, out_channel, now)
        
    await client.logout()

def lambda_handler(event, context):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()

if not 'LAMBDA' in environ:
    lambda_handler(None, None)
