# Import discord.py. Allows access to discord's API
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
load_dotenv()

# grab the API token from the .env file
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Gets the client object from discord.py. Client is synonymous with bot
# bot = discord.Client()
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)


@bot.command()
async def move(ctx, member: discord.Member, ch: discord.VoiceChannel):
    await member.move_to(ch)


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
