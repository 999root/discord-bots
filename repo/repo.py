import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup

intents = discord.Intents.default()
intents.members = True  # Enable the 'members' intent

# Create a new bot instance
bot = commands.Bot(command_prefix='@', intents=intents)

# bible
def scrape_repos(username):
    url = f"https://github.com/{username}?tab=repositories"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        repo_list = soup.find_all("div", class_="col-10 col-lg-9 d-inline-block")
        repos = []

        for repo in repo_list:
            repo_name = repo.find("a").get_text().strip()
            repo_link = f"https://github.com/{username}/{repo_name}"
            terminal_text = f"[{repo_name}]({repo_link})"
            repos.append(terminal_text)

        return repos
    else:
        return "Failed to scrape Github repos."

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
        # Get the mentioned users in the message
        mentioned_users = message.mentions

        # Find the bot's mention in the list
        bot_mention = next((user for user in mentioned_users if user == bot.user), None)

        # If the bot has been mentioned
        if bot_mention is not None:

            # Get the index of the bot's mention
            bot_mention_index = mentioned_users.index(bot_mention)

            # Check if there is a username mentioned after the bot's mention
            if bot_mention_index < len(message.content.split()) - 1:

                # Get the username entered after mentioning the bot
                username = message.content.split()[bot_mention_index + 1]

                # Generate repos based on the entered username
                repos = scrape_repos(username)

                # Check if repositories are found
                if repos:

                    # Iterate through the repos to send a response message
                    for repo in repos:
                        
                        # Send a response to the message
                        await message.channel.send(repo)
                else:
                    await message.channel.send("No repositories found for the provided username.")
            else:
                # No username entered after mentioning the bot
                await message.channel.send("Please provide a GitHub username after mentioning the bot.")



    # Process any other commands or events
    await bot.process_commands(message)

# Run the bot
bot.run("THE BOT'S TOKEN")

# inv link -> https://discord.com/api/oauth2/authorize?client_id=1113029016379740180&permissions=1634772449344&scope=bot