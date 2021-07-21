"""
Discord Docs
https://github.com/Rapptz/discord.py/tree/v1.7.3/examples
"""

import os
import discord
from replit import db
from server import keep_alive

from bot import KAI
from configs import get_config

# Discord client
client = discord.Client()

# KAI initilization
config = get_config("KAI")
bot = KAI(config)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Process message and get response 
    response, reply = bot.response(message)

    if response is not None:
        if isinstance(response, discord.File):
            # Image file
            await message.channel.send(file=response)
        else:
            if reply:   
                # Mention author
                await message.reply(response, mention_author=True)
            else:
                # Send message
                await message.channel.send(response)

        # bot.set_database(message, db)

# Create new processes to keep server online
keep_alive()

# Get user token
TOKEN = os.getenv('TOKEN')

# Start client
client.run(TOKEN)