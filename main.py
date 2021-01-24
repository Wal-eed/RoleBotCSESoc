import os
import time
import discord
from discord.ext import commands
from discord.utils import get


client = commands.Bot(command_prefix="!")
ROLE_CHANNEL_ID = 0
ROLELOG_CHANNEL_ID = 0

@client.event
async def on_ready():
    print('Logged on as {0}!'.format(client.user))


@client.event
async def on_message(message):
    try:
        # Check if the message is in the roles channel, and delete it after completion
        if message.channel.id == ROLE_CHANNEL_ID:
            await client.process_commands(message)
            await message.delete(2)
        else:
            await client.process_commands(message)
    except:
        time.sleep(1.2)
        await message.delete()


# Clear multiple messages in a channel at once, up to 10 at a time.
@client.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, count=3):
    if count > 10:
        count = 10
    await ctx.channel.purge(limit=count)


#Set role channel.
@client.command()
@commands.has_permissions(administrator=True)
async def setrole(ctx):
    global ROLE_CHANNEL_ID
    ROLE_CHANNEL_ID = ctx.channel.id
    await ctx.send(f"Set {ctx.channel} as default role channel.")
    print(f'Set {ROLE_CHANNEL_ID} as default role channel')


# Set role log channel.
@client.command()
@commands.has_permissions(administrator=True)
async def setrolelog(ctx):
    global ROLELOG_CHANNEL_ID
    ROLELOG_CHANNEL_ID = ctx.channel.id
    await ctx.send(f"Set {ctx.channel} as default role log channel.")
    print(f'Set {ROLELOG_CHANNEL_ID} as default role log channel')


# Give user a role.
@client.command()
async def give(ctx, role_input):
    global ROLELOG_CHANNEL_ID
    user = ctx.message.author
    message = ctx.message
    role_input = role_input.upper()
    channel = client.get_channel(ROLELOG_CHANNEL_ID)
    if message.channel.id == ROLE_CHANNEL_ID:
        try:
            role = get(ctx.guild.roles, name=role_input)
            await user.add_roles(role)
            await ctx.message.add_reaction("👍")
            await ctx.send(f'Added {role_input} to {user}')
            await channel.send(f'Added {role_input} to {user}')
        except:
            await ctx.send('Please wait before sending another message. Please make sure your course code '
                           'is joined together. eg:COMP1511')
            await channel.send(f'Failed to add {role_input} to {user}')
            

# Take away user's role.
@client.command()
async def remove(ctx, role_input):
    global ROLELOG_CHANNEL_ID
    channel = client.get_channel(ROLELOG_CHANNEL_ID)

    user = ctx.message.author
    message = ctx.message
    role_input = role_input.upper()
    if message.channel.id == ROLE_CHANNEL_ID:
        try:
            role = get(ctx.guild.roles, name=role_input)
            await user.remove_roles(role)
            await ctx.message.add_reaction("👍")
            await ctx.send(f'Removed {role_input} from {user}')
            await channel.send(f'Removed {role_input} to {user}')
        except:
            await ctx.send('Please wait before sending another message. Please make sure your course code '
                           'is joined together. eg:COMP1511')
            await channel.send(f'Failed to remove {role_input} from {user}')


# Count number of members in a role
@client.command()
@commands.has_permissions(administrator=True)
async def countmembers(ctx, role_name):
    role = get(ctx.guild.roles, name=role_name)
    try:
        await ctx.send(f"`{role_name}` has {len(role.members)} members")
    except:
        await ctx.send(f"`{role_name}` was not found. Please make sure the spelling and capitalisation is correct")


client.run(os.environ['DISCORD_BOT_TOKEN'])
