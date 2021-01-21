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
    await ctx.send(f"Set <#{ROLE_CHANNEL_ID}> as default role channel.")
    print(f'Set {ROLE_CHANNEL_ID} as default role channel')


# Set role log channel.
@client.command()
@commands.has_permissions(administrator=True)
async def setrolelog(ctx):
    global ROLELOG_CHANNEL_ID
    ROLELOG_CHANNEL_ID = ctx.channel.id
    await ctx.send(f"Set <#{ROLELOG_CHANNEL_ID}> as default role log channel.")
    print(f'Set {ROLELOG_CHANNEL_ID} as default role log channel')


# Give user a role.
@client.command()
async def give(ctx, *role_inputs):
    global ROLELOG_CHANNEL_ID
    logchannel = client.get_channel(ROLELOG_CHANNEL_ID)
    user = ctx.message.author
    message = ctx.message
    if message.channel.id == ROLE_CHANNEL_ID:
        for role_input in role_inputs:
            role_input = role_input.upper()
            try:
                role = get(ctx.guild.roles, name=role_input)
                await user.add_roles(role)
                await ctx.send(f'✅ Gave {role_input} to {user}')
                await logchannel.send(f'✅ Gave {role_input} to {user}')
            except:
                await ctx.send(f'❌ Failed to give {role_input} to {user}')
                await logchannel.send(f'❌ Failed to give {role_input} to {user}')


# Take away user's role.
@client.command()
async def remove(ctx, *role_inputs):
    global ROLELOG_CHANNEL_ID
    logchannel = client.get_channel(ROLELOG_CHANNEL_ID)
    user = ctx.message.author
    message = ctx.message
    if message.channel.id == ROLE_CHANNEL_ID:
        for role_input in role_inputs:
            role_input = role_input.upper()
            try:
                role = get(ctx.guild.roles, name=role_input)
                await user.remove_roles(role)
                await ctx.send(f'✅ Removed {role_input} from {user}')
                await logchannel.send(f'✅ Removed {role_input} from {user}')
            except:
                await ctx.send(f'❌ Failed to remove {role_input} from {user}')
                await logchannel.send(f'❌ Failed to remove {role_input} from {user}')


client.run(os.environ['DISCORD_BOT_TOKEN'])
