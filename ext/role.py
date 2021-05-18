import os
import time
import discord
import csv
from discord.ext import commands
from discord.gateway import EventListener
from discord.utils import get, find



class Role(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def countmembers(self,ctx, *role_names):   
        """
        Count the number of members with a certain role 
        """
        roletosearch = " ".join(role_names)

        role = find(lambda r: roletosearch.lower() == r.name.lower(), ctx.guild.roles)
        
        try:
            await ctx.send(f"`{roletosearch}` has {len(role.members)} members")
        except:
            await ctx.send(f"`{roletosearch}` was not found. Please make sure the spelling and capitalisation is correct")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def remove_unverified(self, ctx):
        """
            Admin command to remove all unverified members from the discord.
            Prints out a count of how many unverified members removed. 
            Also gives reason for kick. 
        """
        i = 0
        for member in ctx.guild.members:
            if get(member.roles, name = 'unverified' ):
                i += 1
                await member.send(content = "You have been removed from the CSESoc Server - as you have not verified via the instructions in #welcome")
                await member.kick(reason = "You have been removed from the CSESoc Server - as you have not verified via the instructions in #welcome")
        
        await ctx.send(f"Removed {i} unverified members")
        print(f"Removed {i} unverified members")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def changeprefix(self, ctx, newprefix):
        """
            Change the command prefix during runtime 
        """
        self.client.command_prefix = newprefix
        await ctx.send(f"Set `{newprefix}` as the new command prefix")
        print(f"Set {newprefix} as the new command prefix")


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, count=3):
        """
            Clear multiple messages in a channel at once, up to 10 at a time.
        """
        if count > 10:
            count = 10
        await ctx.channel.purge(limit=count)


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setrole(self, ctx):
        """
            Set role channel
        """
        self.bot.ROLE_CHANNEL_ID = ctx.channel.id
        await ctx.send(f"Set <#{self.bot.ROLE_CHANNEL_ID}> as default role channel.")
        print(f'Set {self.bot.ROLE_CHANNEL_ID} as default role channel')


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setrolelog(self, ctx):
        """
            Set role log channel
        """
        self.bot.ROLELOG_CHANNEL_ID = ctx.channel.id
        await ctx.send(f"Set <#{self.bot.ROLELOG_CHANNEL_ID}> as default role log channel.")
        print(f'Set {self.bot.ROLELOG_CHANNEL_ID} as default role log channel')



    @commands.command()
    async def give(self, ctx, *role_inputs):
        """
            Give user a given role.
        """
        logchannel = self.bot.get_channel(self.bot.ROLELOG_CHANNEL_ID)
        user = ctx.message.author
        message = ctx.message
        success = True
        if message.channel.id == self.bot.ROLE_CHANNEL_ID:
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


    @commands.command()
    async def remove(self, ctx, *role_inputs):
        """
            Take away user's role.
        """
        logchannel = self.bot.get_channel(self.bot.ROLELOG_CHANNEL_ID)
        user = ctx.message.author
        message = ctx.message
        success = True
        if message.channel.id == self.bot.ROLE_CHANNEL_ID:
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


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def bulkgive (self, ctx, role_input):
        """
            Give all the users in a CSV file a specific role
        """
        logchannel = self.client.get_channel(self.bot.ROLELOG_CHANNEL_ID)
        
        members_given = 0
        path = os.getcwd() + '/CSVFile.csv'

        # Get attached CSV file
        attachment_file = ctx.message.attachments[0]
        role = get(ctx.guild.roles, name=role_input)

        # Save file locally
        await attachment_file.save(path)
        
        with open('CSVFile.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                try:
                    user = ctx.guild.get_member_named(row[0])
                    await user.add_roles(role)
                    members_given += 1
                except:
                    await logchannel.send(f'❌ Failed to give {role_input} to {user}')
        
        await logchannel.send(f"Gave {members_given} members the role `{role_input}`")
        
        os.remove(path)


def setup(bot):
    bot.add_cog(Role(bot))




