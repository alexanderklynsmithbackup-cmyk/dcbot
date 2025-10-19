import discord
import os
import threading
from discord.ext import commands
from flask import Flask

intents = discord.Intents.default()
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

WELCOME_CHANNEL_NAME = "💬︱yap"
WELCOME_GIF = "https://media.tenor.com/6TkRi7pddF8AAAAC/anime-welcome.gif"

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_web, daemon=True).start()

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guild(s)')

@bot.event
async def on_member_join(member):
    guild = member.guild
    
    welcome_channel = discord.utils.get(guild.channels, name=WELCOME_CHANNEL_NAME)
    
    if welcome_channel:
        embed = discord.Embed(
            description=f"Hey {member.mention}! Welcome, hope you enjoy your stay!",
            color=discord.Color.blue()
        )
        embed.set_image(url=WELCOME_GIF)
        
        try:
            await welcome_channel.send(embed=embed)
            print(f"Sent welcome message for {member.name} in {guild.name}")
        except Exception as e:
            print(f"Error sending welcome message: {e}")
    else:
        print(f"Welcome channel '{WELCOME_CHANNEL_NAME}' not found in {guild.name}")

token = os.getenv('DISCORD_BOT_TOKEN')
if token:
    bot.run(token)
else:
    print("Error: DISCORD_BOT_TOKEN not found in environment variables")
    print("Please add your Discord bot token to Replit Secrets")
