import os
import discord
from replit import db
from server import keep_alive

from bot import KAI
from configs import get_config

client = discord.Client()

config = get_config("KAI")
bot = KAI(config)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    response, reply = bot.response(message)

    if response is not None:
        if isinstance(response, discord.File):
            await message.channel.send(file=response)
        else:
            if reply:   
                await message.reply(response, mention_author=True)
            else:
                await message.channel.send(response)

        # bot.set_database(message, db)


keep_alive()
TOKEN = os.getenv('TOKEN')
client.run(TOKEN)