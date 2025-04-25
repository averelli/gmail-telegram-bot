# Gmail Telegram Bot

A Telegram bot that sends a user defined notification when an email from a specific sender appears in the inbox. 

## Features

- **Email Notifications**: Get Telegram notifications when emails are received from specific senders
- **Keyword Filtering**: Configure the bot to only notify about emails containing specific keywords
- **Easy Configuration**: Simple commands to add/remove tracked email addresses and keywords
- **Gmail Integration**: Securely connects to a Gmail account using OAuth

## Configuration

1. From the Google Cloud Platform get OAuth 2.0 JSON credentials, rename the file to `credentials.json` and place it in the project secrets directory

2. Create a `.env` file in the project secrets direcotory with the Telegram bot token

3. Run `bot.py` to start the bot for the first time and send `/refresh` to set the chat id inside the config, press Ctrl+C to stop the bot

4. In the `config/config.json` set up the polling interval at which the app will check the inbox, by default every 30 minutes

## Usage

### Starting the Bot

Run the app with:
```
python main.py
```

The first time it will open a Google sign in page to get access to user's Gmail

### Telegram Commands

The bot responds to the following commands:

- `/refresh` - Should be the very first command to set up the correct chat id
- `/help` - Display available commands and their usage
- `/add` - Start the add new query flow to add a new email and keywords to look for and set up a custom notification
- `/del` - Delete one of the existing queries
- `/list` - Display existing queries