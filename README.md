# Sopel AI Chatbot

This Sopel module allows your IRC bot to interact with OpenAI's GPT-3.5-turbo model to provide AI-generated responses to user queries.

## Features

- Responds to user queries prefixed with `ai:`
- Splits long responses into manageable chunks for IRC
- Logs errors for troubleshooting

## Prerequisites

- Python 3.6 or higher
- Sopel IRC Bot
- OpenAI API key

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/lord3nd3r/sopel-ai-chatbot.git
    cd sopel-ai-chatbot
    ```

2. **Install the required packages:**

    ```bash
    pip install requests sopel
    ```

3. **Configure Sopel:**

    Ensure that your Sopel bot is configured and running. Follow the Sopel [documentation](https://sopel.chat/docs/) for setup instructions.

4. **Add the module to your Sopel bot:**

    Copy the `ai_chatbot.py` file to your Sopel modules directory (usually `~/.sopel/modules`).

5. **Set your OpenAI API key:**

    Replace `your_openai_api_key_here` in the code with your actual OpenAI API key.

## Usage

- **Trigger the AI response:**

    In the IRC channel, type `ai: your_query_here` to get a response from the AI. The bot will respond in chunks if the response is too long.

## Code Explanation

### chatgpt_response(bot, trigger)

This function is triggered when a message starting with `ai:` is detected. It extracts the query, gets a response from the AI, and sends the response back to the IRC channel in chunks.

### get_chatgpt_response(query)

This function sends a request to the OpenAI API with the user's query and returns the response. It handles API errors and rate limits.

### split_into_chunks(text, max_length)

This helper function splits the AI response into chunks that fit within the maximum message length for IRC.

## Logging

Errors and important events are logged using Python's logging module. Check your Sopel bot's logs for details.

## License

This project is licensed under the MIT License.

## Contributing

Feel free to open issues or submit pull requests. Contributions are welcome!

