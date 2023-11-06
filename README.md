# Discord Bot with OpenAI Integration

This is a discord bot that uses application commands (slash commands). It has several commands such as generating a social media post, providing information about the bot, listing all available commands, and retrieving the last 10 messages from a specified channel. The social media post command uses OpenAI's GPT-3 model to generate a post based on a given raw text. The generated post can be approved, cancelled, or regenerated using buttons.

## Setup Instructions

Follow these steps to set up the environment for your bot:

### 1. Create a Discord Bot

Set up your Discord bot in the [Discord Developer Portal](https://discord.com/developers/applications). Here, you will generate your bot token to be used in your `.env` file.

### 2. Obtain OpenAI Key

Register on the [OpenAI website](https://beta.openai.com/signup/) to obtain your API key.

### 3. Get Channel ID and Guild ID

Enable Developer Mode in your Discord settings to obtain your Channel ID and Guild ID (also known as the Discord Server ID). There are numerous guides and YouTube tutorials available online to assist you in this process.

## Hosting

This bot can be hosted on Replit or Azure App Service which both handle "secrets" (i.e., environment variables) within their web interface.

If you plan to host the bot elsewhere, you will need to:

- Include the following code in your script:

    ```python
    from dotenv import load_dotenv
    load_dotenv()
    ```

- Install `python-dotenv` using pip from your terminal:

    ```bash
    pip install python-dotenv
    ```

- Create your own `.env` file that defines `OPENAI_API_KEY`, `GUILD_ID`, `CHANNEL_ID`, and `DISCORD_TOKEN`. The file should look like this:

    ```bash
    OPENAI_API_KEY=your_openai_api_key
    GUILD_ID=your_guild_id
    CHANNEL_ID=your_channel_id
    DISCORD_TOKEN=your_discord_token
    ```

Replace `your_openai_api_key`, `your_guild_id`, `your_channel_id`, and `your_discord_token` with your actual values. 

**IMPORTANT**: Do not commit your `.env` file to your public GitHub repository or any other public platform. It's best practice to add `.env` to your `.gitignore` file to avoid accidentally committing it.
