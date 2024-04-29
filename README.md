# Pat Bot

This is a Discord bot that responds to messages matching a certain regex pattern. The bot is built using the discord.py library.

## Features

- Responds to any message that matches a certain regex pattern with a "*pats*" message.
- Deletes messages from certain users that do not match the regex pattern.
- Logs when and by whom the bot is activated.

## Setup

1. Clone this repository.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Create a `.env` file in the root directory of the project and add the following environment variables:
    - `TOKEN`: Your Discord bot token.
    - `DISALLOWED_IDS`: A comma-separated list of user IDs that the bot should delete messages from if they do not match the regex pattern.
4. Run the bot by executing `python pat.py`.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
