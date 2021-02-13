# RoleBotCSESoc
A role bot to manage roles for the CSESoc discord.
## Table of contents
* [Setup](#setup)
* [Commands](#commands)
	
## Setup
* Please set an environment variable named `DISCORD_BOT_TOKEN` and assign it your Discord application token.
* Please enable server member intents for your bot application by going to the Discord developer portal > Your bot application (under My Applications) > Bot and enabling it under the "Privileged Gateway Intents" section. This step is required for *** features to work. This intent is disabled by default.
* Use the command ```!setrole``` to set the channel you want the bot to be active in.
* Use the command ```!setrolelog``` to set the channel you want the bot to log all of its activities in.

Only users with administrator privileges can use these commands.

## Commands 

##### ```!give ROLE1 ROLE2 ROLE3 ...``` : Gives the specified role(s) to the user.
##### ```!remove ROLE1 ROLE2 ROLE3 ...``` : Removes the specified role(s) from the user.
##### ```!countmembers ROLE```* : Counts the number of members with the specified role.
##### ```!clear VALUE``` : Clears multiple messages at once in the channel the command is used in, up to a maximum of 10 at a time. Only users with administrator privileges can use this.
##### ```!changeprefix NEWPREFIX``` : Changes the default command prefix from '!' to NEWPREFIX. (*Example:`!changeprefix +` will make all future commands only run when the prefix is '+'*). Only users with administrator privileges can use this.

*Note: If you run !changeprefix command, all commands mentioned here will be called using the new prefix, not '!'*.
