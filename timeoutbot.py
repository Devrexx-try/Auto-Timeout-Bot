import discord
from discord.ext import commands
from datetime import timedelta

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

SPECIFIC_USER_IDS = [USER_ID-1, USER_ID-2]
TIMEOUT_DURATION = 600

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.mentions and any(user.id in SPECIFIC_USER_IDS for user in message.mentions):
        try:
            timeout_duration = timedelta(seconds=TIMEOUT_DURATION)
            await message.author.timeout(timeout_duration, reason="Mentioned a restricted user.")
            await message.channel.send(f"{message.author.mention} has been timed out for mentioning a restricted user.")
        except discord.Forbidden:
            await message.channel.send("I do not have permission to timeout this member.")
        except discord.HTTPException:
            await message.channel.send("Failed to timeout the user.")
    
    await bot.process_commands(message)

bot.run('ENTER_YOUR_TOKEN')
