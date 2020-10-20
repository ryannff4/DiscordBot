# Import discord.py. Allows access to discord's API
import discord
import os
import json
import pprint
from dotenv import load_dotenv
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
load_dotenv()

MEMBER_DATA_FILE = 'memberData.json'
memberData = {}
with open(MEMBER_DATA_FILE, 'r') as memberDataFile:
    memberData = json.load(memberDataFile)

# leadershipList = memberData.get("Leadership")
# membersList = memberData.get("Members")
# grab the API token from the .env file
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Gets the client object from discord.py. Client is synonymous with bot
# bot = discord.Client()
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.command()
async def addtoroster(ctx, member: discord.Member, role):
    memberNickname = member.display_name
    splitName = memberNickname.split("(")
    memberFirstName = splitName[0]
    listData = memberData.get(role.title())

    newMemberDictData = {}
    newMemberDictData['Nickname'] = memberNickname
    newMemberDictData['Name'] = memberFirstName

    listData.append(newMemberDictData)

    memberData[role.title()] = listData

    with open(MEMBER_DATA_FILE, 'w') as updatedMemberDataFile:
        jsonData = json.dumps(memberData)
        updatedMemberDataFile.write(jsonData)


@bot.command()
async def showroster(ctx):
    outputString = ""
    for k in memberData.keys():
        outputString = outputString + k + ":\n"
        for v in memberData[k]:
            outputString = outputString + "\t" + v["Name"] + "\n"
    await ctx.send(outputString)

'''
commands.Greedy: https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Greedy

async def foo(ctx, arg1, arg2, *args):
    ...

# Invoking "?foo one two three four" will have
# arg1 = 'one'
# arg2 = 'two'
# args = ('three', 'four')

async def bar(ctx, arg1, arg2, *, args):
    ...

# Invoking "?bar one two three four" will have
# arg1 = 'one'
# arg2 = 'two'
# args = 'three four'
'''
@bot.command()
async def move(ctx, members: commands.Greedy[discord.Member], *, ch: discord.VoiceChannel):
    for member in members:
        await member.move_to(ch)


@bot.command()
async def muteall(ctx):
    vc = ctx.author.voice.channel
    for member in vc.members:
        await member.edit(mute=True)


@bot.command()
async def unmuteall(ctx):
    vc = ctx.author.voice.channel
    for member in vc.members:
        await member.edit(mute=False)


@bot.command(pass_context=True)
async def addrole(ctx, user: discord.Member, role: discord.Role):
    try:
        await user.add_roles(role)
        await ctx.send(f"{user.name} has been given a role called {role.name}")
    except Exception as e:
        await ctx.send("There was an error running this command: " + str(e))


@bot.command(pass_context=True)
async def removerole(ctx, user: discord.Member, role: discord.Role):
    try:
        await user.remove_roles(role)
        await ctx.send(f"{user.name} has had role {role.name} removed")
    except Exception as e:
        await ctx.send("There was an error running this command: " + str(e))


# event listener for when the bot has switched from offline to online
@bot.event
async def on_ready():
    # creates a counter to keep track of how many servers the bot is connected to
    guild_count = 0

    # loops through all the servers the bot is associated with
    for guild in bot.guilds:
        # print the server's ID and name
        print(f"- {guild.id} (name: {guild.name})")

        guild_count += 1

    print("ExperimentalPythonBot is in " + str(guild_count) + " guilds.")


# event listener for when a new message is sent to a channel
@bot.event
async def on_message(message):
    # checks if the message that was sent is equal to "hello"
    if "experimentalpythonbot" in message.content.lower():
        # sends back a message to the channel
        await message.channel.send("hey dirtbag")

    await bot.process_commands(message)

# execute the bot with the specific token
bot.run(DISCORD_TOKEN)
