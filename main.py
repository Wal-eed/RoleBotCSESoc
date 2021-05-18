import os
import time
import discord
import csv
from discord.ext import commands
from discord.utils import get, find


# Enables custom intents and explicitly allows access to members
intents = discord.Intents.default()  
intents.members = True

client = commands.Bot(command_prefix="!", intents=intents)   
client.load_extension('ext.role')         

client.ROLE_CHANNEL_ID = 0
client.ROLELOG_CHANNEL_ID = 0
client.VERFIED_ROLE = "unverified"

@client.event
async def on_ready():
    print('Logged on as {0}!'.format(client.user))

@client.event
async def on_message(message):
    try:
        # Check if the message is in the roles channel, and delete it after completion
        if message.channel.id == client.ROLE_CHANNEL_ID:
            await client.process_commands(message)
            await message.delete(2)
        else:
            await client.process_commands(message)
    except:
        time.sleep(1.2)
        await message.delete()

if __name__ == '__main__':
    client.run(os.environ['DISCORD_BOT_TOKEN'])

