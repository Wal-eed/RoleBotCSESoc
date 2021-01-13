import os
import time
import discord
from discord.ext import commands
from discord.utils import get


client = commands.Bot(command_prefix="!")
role_channel_id = 0
rolelog_channel_id = 0

@client.event
async def on_ready():
    print('Logged on as {0}!'.format(client.user))


@client.event
async def on_message(message):
    try:
        # Check if the message is in the roles channel, and delete it after completion
        if message.channel.name == 'roles':
            await client.process_commands(message)
            await message.channel.purge(limit=1)
        else:
            await client.process_commands(message)
    except:
        time.sleep(1.2)
        await message.channel.purge(limit=1)


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
    global role_channel_id
    role_channel_id = ctx.channel.id
    await ctx.send(f"Set {ctx.channel} as default role log channel.")
    print(f'Set{role_channel_id} as default role log channel')


# Set role log channel.
@client.command()
@commands.has_permissions(administrator=True)
async def setrolelog(ctx):
    global rolelog_channel_id
    rolelog_channel_id= ctx.channel.id
    await ctx.send(f"Set {ctx.channel} as default role log channel.")
    print(f'Set{rolelog_channel_id} as default role log channel')


# Give user a role.
@client.command()
async def give(ctx, role_input):
    global rolelog_channel_id
    user = ctx.message.author
    message = ctx.message
    role_input = role_input.upper()
    channel = client.get_channel(rolelog_channel_id)

    try:
        role = get(ctx.guild.roles, name=role_input)
        await user.add_roles(role)
        await ctx.message.add_reaction("👍")
        await ctx.send(f'Added {role_input} to {user}')
        await channel.send(f'Added {role_input} to {user}')
        time.sleep(1)
    except:
        await ctx.send('Please wait before sending another message. Please make sure your course code '
                       'is joined together. eg:COMP1511')
        await channel.send(f'Failed to add {role_input} to {user}')
        time.sleep(2)


# Take away user's role.
@client.command()
async def remove(ctx, role_input):
    global rolelog_channel_id
    channel = client.get_channel(rolelog_channel_id)

    user = ctx.message.author
    role_input = role_input.upper()
    try:
        role = get(ctx.guild.roles, name=role_input)
        await user.remove_roles(role)
        await ctx.message.add_reaction("👍")
        await ctx.send(f'Removed {role_input} from {user}')
        await channel.send(f'Removed {role_input} to {user}')
        time.sleep(1)
    except:
        await ctx.send('Please wait before sending another message. Please make sure your course code '
                       'is joined together. eg:COMP1511')
        await channel.send(f'Failed to remove {role_input} from {user}')
        time.sleep(2)


client.run(os.environ['DISCORD_BOT_TOKEN'])
