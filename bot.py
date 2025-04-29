# bot.py - Fixed version
import discord
from discord.ext import commands
import os
import json
import random
import asyncio
from dotenv import load_dotenv
from chatbot_trainer import chatbot

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
OWNER_ID = int(os.getenv('OWNER_ID'))  # Add your Discord ID to .env

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
active_trivia_sessions = {}

# Load quotes
try:
    with open('data/quotes.json', 'r') as f:
        quotes = json.load(f)['quotes']
except (FileNotFoundError, json.JSONDecodeError):
    quotes = ["Backup quote: Keep learning!"]

TRIVIA_QUESTIONS = [
    {"q": "What is the capital of France?", "a": "Paris"},
    {"q": "What planet is known as the Red Planet?", "a": "Mars"}
]

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.change_presence(activity=discord.Game(name="!trivia"))

@bot.command(name='restart')
@commands.is_owner()
async def restart(ctx):
    """Restart the bot (Owner only)"""
    await ctx.send("🔄 Restarting...")
    await bot.close()
    # This will exit the script, and you'll need external tools to auto-restart
    
@bot.command(name='shutdown')
@commands.is_owner()
async def shutdown(ctx):
    """Shut down the bot (Owner only)"""
    await ctx.send("⏏️ Shutting down...")
    await bot.close()

@bot.command(name='trivia')
async def trivia(ctx):
    """Start a trivia game"""
    # Add user to active sessions
    active_trivia_sessions[ctx.author.id] = True
    
    question = random.choice(TRIVIA_QUESTIONS)
    await ctx.send(f"**TRIVIA:** {question['q']}")
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    
    try:
        msg = await bot.wait_for('message', timeout=30.0, check=check)
        if msg.content.lower() == question['a'].lower():
            await ctx.send("✅ Correct!")
        else:
            await ctx.send(f"❌ Wrong! Answer: {question['a']}")
    except TimeoutError:
        await ctx.send("⏰ Time's up!")
    finally:
        # Remove user from active sessions
        active_trivia_sessions.pop(ctx.author.id, None)

@bot.command(name='quote')
async def quote(ctx):
    """Get a random quote"""
    await ctx.send(f"📜 {random.choice(quotes)}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    # Only respond with ChatterBot if not in active trivia session
    if (not message.content.startswith('!') 
        and message.author.id not in active_trivia_sessions):
        response = chatbot.get_response(message.content)
        await message.channel.send(str(response))
    
    await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(TOKEN)

if __name__ == "__main__":
    try:
        bot.run(TOKEN)
    except KeyboardInterrupt:
        print("\nBot terminated by user")
    finally:
        print("Cleaning up resources...")