# RoleBotCSESoc
A role bot to manage roles for the CSESoc discord.
## Table of contents
* [Setup](#setup)
* [Commands](#commands)
	
## Setup
Please set an enviorment variable named `DISCORD_BOT_TOKEN` and assign it your Discord application token.
Use the command ```!setrole``` to set the channel you want the bot to be active in.
Use the command ```!setrolelog``` to set the channel you want the bot to log all of its activities active in.
Only users with administrator privileges can use these commands.

## Commands

##### ```!give ROLE``` : Gives the user the specified role.
##### ```!remove ROLE``` : Removes the specified role.
##### ```!clear VALUE``` : Clears multiple messages at once in the channel the command is used in, up to a maximum of 10 at a time. Only users with administrator privileges can use this.
