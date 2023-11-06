# Import the required packages
import discord
import os
import openai
import logging
from dotenv import load_dotenv
from keep_alive import keep_alive
from discord import app_commands
from discord import ButtonStyle
from discord.ui import Button, View

# Configures the logging module
logging.basicConfig(level=logging.INFO)

# Load environment variables from .env file
load_dotenv()

# Create intents object to handle events on Discord
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# Initialize the Discord client with the intents
client = discord.Client(intents=intents)

# Create a CommandTree for handling slash commands
tree = app_commands.CommandTree(client)

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Variable to handle message state
handling_message = False

# Event handler for when the bot is ready
@client.event
async def on_ready():
    logging.info('Bot is starting up...')
    print(f'We have logged in as {client.user}')
    tree.copy_global_to(guild=discord.Object(id=os.getenv("GUILD_ID")))
    await tree.sync(guild=discord.Object(id=os.getenv("GUILD_ID")))

# Class for handling Post button views
class PostButtonsView(View):
    def __init__(self, raw_text, original_interaction, latest_post):
        super().__init__()
        self.raw_text = raw_text
        self.original_interaction = original_interaction
        self.latest_post = latest_post

    # Button for approving a post
    @discord.ui.button(style=ButtonStyle.success, label='Approve')
    async def approve(self, interaction: discord.Interaction, button: Button):
        logging.info('Approve button pressed...')
        await interaction.response.edit_message(
            content=f"{self.latest_post}\n\nThis functionality is TBD! In the meantime, feel free to submit another entry to be converted to a twitter post and posted.",
            view=None
        )

    # Button for cancelling a post
    @discord.ui.button(style=ButtonStyle.danger, label='Cancel')
    async def cancel(self, interaction: discord.Interaction, button: Button):
        logging.info('Cancel button pressed...')
        await interaction.response.edit_message(
            content=f"{self.latest_post}\n\nProcess cancelled. Please submit another entry to be converted to a twitter post.",
            view=None
        )

    # Button for regenerating a post
    @discord.ui.button(style=ButtonStyle.secondary, label='Regenerate')
    async def regenerate(self, interaction: discord.Interaction, button: Button):
        logging.info('Regenerate button pressed...')
        response = get_ai_response(self.raw_text)
        summarized_message = response['choices'][0]['message']['content']
        self.latest_post = summarized_message
        await interaction.response.edit_message(
            content=f"{summarized_message}\n\nShould I post this?", 
            view=self
        )

# Command for generating a post
@tree.command(description='Generate a social media post. Please provide the raw text to be summarized into the twitter post.')
async def generate_post(interaction: discord.Interaction, raw_text: str):
    logging.info('Generating post...')
    response = get_ai_response(raw_text)
    summarized_message = response['choices'][0]['message']['content']

    view = PostButtonsView(raw_text, interaction, summarized_message)
    await interaction.response.send_message(
        f"{summarized_message}\n\nShould I post this?", view=view
    )

# Function to get response from OpenAI
def get_ai_response(content):
  logging.info('Requesting AI response from OpenAI...')
  return openai.ChatCompletion.create(
    model="gpt-3.5-turbo-16k-0613",
    messages=[{
      "role": "system",
      "content": "You are a helpful social media manager. Your job is to generate an engaging, SEO optimized social media content. Given the following message content from the user, please generate a Twitter post, less than 250 characters, with 2-3 hashtags, 1 or 2 emojis, no quotes. Respond with no other text than the post itself:"
    }, {
      "role": "user",
      "content": content
    }])

# Command to list all available commands
@tree.command(description='List of commands')
async def help(interaction: discord.Interaction):
    # Send a message back to the user with the list of all available commands
    await interaction.response.send_message("""
This bot is a WiP. Here is the list of all available commands:
/help - Lists all commands
/generate_post - Generates social media post based off of your text. Prompt is hard-coded at the moment. Posting is WiP.
/get_messages - Returns last 10 messages when provided a channel ID in this format: 9351494256651961317 (need to turn on developer mode to get the channel ID)
""")

# Command to retrieve the last 10 messages from a specified channel
@tree.command(description='Retrieve the last 10 messages from a specified channel')
async def get_messages(interaction: discord.Interaction, channel_id: str):
    logging.info('Retrieving messages...')
    # Get the channel from the channel_id provided by the user
    channel = client.get_channel(int(channel_id))
    if channel is None:
        # Send a message back to the user if the channel does not exist
        await interaction.response.send_message('The specified channel does not exist.')
        return

    messages = []
    # Asynchronously iterate over the history of the channel, collecting up to 10 messages
    async for message in channel.history(limit=10):
        messages.append(message)

    # Send the first message as the initial response
    first_message = messages[0]
    formatted_message = f"{first_message.author}: {first_message.content}"
    if len(formatted_message) > 2000:
        formatted_message = formatted_message[:2000]
    await interaction.response.send_message(formatted_message)

    # Send all other messages as follow-ups
    for message in messages[1:]:
        formatted_message = f"{message.author}: {message.content}"
        if len(formatted_message) > 2000:
            formatted_message = formatted_message[:2000]
        await interaction.followup.send(formatted_message)

# Call the function from keep_alive.py to keep the bot running
keep_alive()

# Get the Discord bot token from environment variable and run the bot
token = os.getenv("TOKEN")
client.run(token)
