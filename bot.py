import discord
from discord.ext import commands
import os

TOKEN = 'YOUR_TOKEN_HERE'  # Still hardcoded 

intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')  
    # TODO: Load trivia questions from file later

@bot.command(name='trivia')
async def trivia(ctx):
    await ctx.send("Placeholder")  # Placeholder
    # TODO: Fetch random question from API 

@bot.command(name='quote')
async def quote(ctx):
    await ctx.send("Placeholder")  # Broken feature
    # TODO: Connect to Quotes API

if __name__ == "__main__":
    bot.run(TOKEN)  