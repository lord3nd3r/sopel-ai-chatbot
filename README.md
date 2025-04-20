# Sopel AI-OpenAI Plugin

Transform your Sopel IRC bot into a Linux wizard, hardcore prepper, and coding guru with a razor-sharp wit and an encyclopedia’s worth of knowledge! Powered by OpenAI’s ChatGPT, this plugin dishes out practical, snarky answers—whether you’re debugging a bash script, prepping for the end of days, or craving a Linux-themed zinger. It’s like having a sysadmin, survivalist, and comedian chilling in your IRC channel.

## Features

- **OpenAI Integration**: Harnesses ChatGPT (e.g., `gpt-4o-mini`) for dynamic, context-aware replies.
- **Themed Persona**: Blends Linux expertise, prepper grit, and developer savvy with playful sarcasm.
- **Custom Jokes**: Delivers short, witty Linux, programming, or prepper-themed jokes on demand.
- **Conversation History**: Tracks up to 50 messages per channel for coherent chats.
- **Rate Limiting**: Caps API calls at 1 per 5 seconds per channel to keep things cool.
- **Message Splitting**: Chops long replies into IRC-friendly 450-character chunks.
- **Reset Command**: Wipes conversation history with a `.reset` command, Arch-style.

## Prerequisites

- Python 3.8+ (tested on 3.12)
- [Sopel](https://sopel.chat/) (`pipx install sopel`)
- OpenAI Python Client (`pipx runpip sopel install openai`)
- OpenAI API Key from [OpenAI’s platform](https://platform.openai.com/account/api-keys)
- Access to an IRC server (e.g., Libera.Chat) where your bot has permissions

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/lord3nd3r/sopel-ai-chatbot.git
   cd sopel-ai-openai
   ```

2. **Install the Plugin**:
   Copy `ai-openai.py` to Sopel’s plugin directory:
   ```bash
   mkdir -p ~/.sopel/plugins
   cp ai-openai.py ~/.sopel/plugins/
   chmod 644 ~/.sopel/plugins/ai-openai.py
   ```

3. **Install Dependencies**:
   Ensure Sopel and OpenAI are installed:
   ```bash
   pipx install sopel
   pipx runpip sopel install openai
   ```

## Configuration

You **must** configure Sopel’s `default.cfg` with a `chat` section to include your OpenAI API key and optional settings. Here’s how to set it up:

1. **Edit the Config**:
   Open or create `~/.sopel/default.cfg`:
   ```bash
   nano ~/.sopel/default.cfg
   ```

2. **Add Required Settings**:
   Add the `[core]` and `[chat]` sections:
   ```ini
   [core]
   nick = ascii
   host = irc.libera.chat
   use_ssl = true
   port = 6697
   owner = yournick
   channels = #yourchannel
   plugins = chat
   loglevel = DEBUG

   [chat]
   api_key = sk-your-openai-api-key  # Your OpenAI API key (required)
   model = gpt-4o-mini  # Options: gpt-3.5-turbo-0125, gpt-4-turbo-2024-04-09, gpt-4o-mini
   history_limit = 50  # Max messages stored per channel
   max_message_length = 450  # Max characters per IRC message
   message_delay = 1.0  # Seconds between split messages
   ```

   **Note**: Replace `sk-your-openai-api-key` with your actual OpenAI API key from [OpenAI](https://platform.openai.com/account/api-keys). No key, no chat—your bot will just sit there like a bricked server.

3. **Optional Settings**:
   - `model`: Pick a beefier OpenAI model (note: costs more).
   - `history_limit`: Tweak for more/less conversation context.
   - `max_message_length`: Adjust for your IRC server’s limits.
   - `message_delay`: Increase to avoid spam flags on strict servers.

4. **Save and Secure**:
   Save the file and restrict permissions:
   ```bash
   chmod 600 ~/.sopel/default.cfg
   ```

## Usage

1. **Start Sopel**:
   ```bash
   sopel --config ~/.sopel/default.cfg
   ```

2. **Interact with the Bot**:
   Address the bot by its nick (e.g., `ascii`) in your IRC channel:
   - Ask a question:
     ```
     ascii: How do I harden my Linux server?
     ```
     *Response*: “Lock it down with `ufw`, ban root logins, and pray nobody runs `sudo rm -rf /`. Want a config guide?”
   - Request a joke:
     ```
     ascii tell me a joke
     ```
     *Response*: “Why do preppers love bash scripts? One `cron` job and your bunker’s stocked for the apocalypse!”
   - Clear history:
     ```
     ascii: reset
     ```
     *Response*: “Conversation history wiped cleaner than a fresh Arch install!”

3. **Supported Commands**:
   - **Nick-Prefixed Messages**: `ascii <message>`, `ascii: <message>`, `ascii, <message>` (e.g., `ascii debug my Python code`).
   - **Reset**: `.reset` (channel-only, clears conversation history).

## Troubleshooting

- **Bot Not Responding**:
  - Check logs for errors:
    ```bash
    tail -f ~/.sopel/logs/sopel.log
    ```
  - Verify your OpenAI API key is valid (test with OpenAI’s Python client).
  - Confirm the `chat` plugin is loaded:
    ```
    .plugins
    ```

- **Responses Not Themed**:
  - Clear old context:
    ```
    ascii: reset
    ```
  - Ensure `model` in `default.cfg` supports complex prompts (e.g., `gpt-4o-mini`).

- **Rate Limit Errors**:
  - Seeing “rationing brainpower”? Wait 5 seconds or check your OpenAI quota at [OpenAI](https://platform.openai.com/usage).

- **Plugin Not Loading**:
  - Verify `ai-openai.py` is in `~/.sopel/plugins/` and readable:
    ```bash
    ls -l ~/.sopel/plugins/ai-openai.py
    ```
  - Check `plugins = chat` in `default.cfg`.

## Contributing

Want to make this bot tougher than a bunker in a storm? Fork, hack, and send a pull request! Ideas:
- Local joke cache to cut API costs.
- `ascii: debug <code>` for code fixes.
- `ascii: prepper tip` for survival nuggets.

To contribute:
1. Fork and clone:
   ```bash
   git clone https://github.com/yourusername/sopel-ai-openai.git
   ```
2. Create a branch:
   ```bash
   git checkout -b feature/awesome-addition
   ```
3. Commit changes:
   ```bash
   git commit -m "Add awesome feature"
   ```
4. Push and open a PR:
   ```bash
   git push origin feature/awesome-addition
   ```

## License

MIT License. See [LICENSE](LICENSE) for details.

## Acknowledgments

- Powered by [Sopel](https://sopel.chat/) and [OpenAI](https://openai.com/).
- For IRC legends who live by the terminal and prep for the end of the world.
