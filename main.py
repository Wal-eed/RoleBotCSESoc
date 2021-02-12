import os
import time
import discord
from discord.ext import commands
from discord.utils import get


# Enables custom intents and explicitly allows access to members
intents = discord.Intents.default()  
intents.members = True


client = commands.Bot(command_prefix="!", intents=intents)
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


# Count the number of members with a certain role 
@client.command()
@commands.has_permissions(administrator=True)
async def countmembers(ctx, role_name):
    role = get(ctx.guild.roles, name=role_name)
    try:
        await ctx.send(f"`{role_name}` has {len(role.members)} members")
    except:
        await ctx.send(f"`{role_name}` was not found. Please make sure the spelling and capitalisation is correct")


# Change the command prefix during runtime 
@client.command()
@commands.has_permissions(administrator=True)
async def changeprefix(ctx, newprefix):
    client.command_prefix = newprefix
    await ctx.send(f"Set `{newprefix}` as the new command prefix")
    print(f"Set {newprefix} as the new command prefix")


# Clear multiple messages in a channel at once, up to 10 at a time.
@client.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, count=3):
    if count > 10:
        count = 10
    await ctx.channel.purge(limit=count)


# Set role channel.
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
    success = True
    if message.channel.id == ROLE_CHANNEL_ID:
        for role_input in role_inputs:
            role_input = role_input.upper()
            try:
                role = get(ctx.guild.roles, name=role_input)
                await user.add_roles(role)
                await ctx.send(f'✅ Gave {role_input} to {user}')
                await logchannel.send(f'✅ Gave {role_input} to {user}')
            except:
                await ctx.send(f'❌ Failed to give {role_input} to {user}. Please make sure your course code matches exactly e.g. `COMP1511` not `COMP 1511`')
                await logchannel.send(f'❌ Failed to give {role_input} to {user}')
                success = False
        if success:
            await ctx.message.add_reaction("👍")


# Take away user's role.
@client.command()
async def remove(ctx, *role_inputs):
    global ROLELOG_CHANNEL_ID
    logchannel = client.get_channel(ROLELOG_CHANNEL_ID)
    user = ctx.message.author
    message = ctx.message
    success = True
    if message.channel.id == ROLE_CHANNEL_ID:
        for role_input in role_inputs:
            role_input = role_input.upper()
            try:
                role = get(ctx.guild.roles, name=role_input)
                await user.remove_roles(role)
                await ctx.send(f'✅ Removed {role_input} from {user}')
                await logchannel.send(f'✅ Removed {role_input} from {user}')
            except:
                await ctx.send(f'❌ Failed to remove {role_input} from {user}. Please make sure your course code matches exactly e.g. `COMP1511` not `COMP 1511`')
                await logchannel.send(f'❌ Failed to remove {role_input} from {user}')
                success = False
        if success:
            await ctx.message.add_reaction("👍")


client.run(os.environ['DISCORD_BOT_TOKEN'])