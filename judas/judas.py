import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup

intents = discord.Intents.default()
intents.members = True  # Enable the 'members' intent

# Create a new bot instance
bot = commands.Bot(command_prefix='@', intents=intents)

# bible
def scrape_bible_verse():
    url = "https://dailyverses.net/random-bible-verse"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        verses = soup.find_all("span", class_="v1")
        return [verse.get_text() for verse in verses]
    else:
        return "Failed to scrape Bible verses."

# Event triggered when the bot is ready and connected to Discord
@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user.name}')

# Event triggered when a message is received
@bot.event
async def on_message(message):
    # Ignore messages sent by the bot itself to avoid infinite loops
    if message.author == bot.user:
        return

    # Check if the bot is mentioned in the message
    if bot.user in message.mentions:

        # Generate verse
        bible_verse = scrape_bible_verse()

        # Itterate through the verse to remove unwanted strings
        for verse in bible_verse:

            # Send a response to the message
            await message.channel.send(verse)

    # Process any other commands or events
    await bot.process_commands(message)

# Run the bot
bot.run("THE BOT'S TOKEN") # nt