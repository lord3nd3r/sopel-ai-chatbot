Sopel AI-OpenAI Plugin
Turn your Sopel IRC bot into a Linux wizard, hardcore prepper, and coding guru with a sharp wit and an encyclopedia’s worth of knowledge! Powered by OpenAI’s ChatGPT, this plugin delivers practical answers with a rugged, self-reliant edge, whether you’re debugging a bash script, prepping for the apocalypse, or just craving a snarky Linux joke. It’s like having a sysadmin, survivalist, and stand-up comedian in your IRC channel.
Features

OpenAI-Powered Responses: Harnesses ChatGPT (e.g., gpt-4o-mini) for dynamic, context-aware replies.
Themed Persona: Blends Linux expertise, prepper grit, and developer savvy with playful sarcasm.
Custom Jokes: Serves up short, witty Linux, programming, or prepper-themed jokes on demand.
Conversation History: Tracks up to 50 messages per channel for coherent chats.
Rate Limiting: Caps API calls at 1 per 5 seconds per channel to keep things chill.
Message Splitting: Chops long replies into IRC-friendly 450-character chunks.
Reset Command: Wipes conversation history with a .reset command, Arch-style.

Prerequisites

Python: 3.8+ (tested on 3.12).
Sopel: Latest version (pipx install sopel).
OpenAI Python Client: pipx runpip sopel install openai.
OpenAI API Key: Grab one from OpenAI’s platform.
IRC Server: A channel where your bot has permissions (e.g., Libera.Chat).

Installation

Clone the Repo:
git clone https://github.com/yourusername/sopel-ai-openai.git
cd sopel-ai-openai


Install the Plugin:Copy ai-openai.py to Sopel’s plugin directory:
mkdir -p ~/.sopel/plugins
cp ai-openai.py ~/.sopel/plugins/
chmod 644 ~/.sopel/plugins/ai-openai.py


Install Dependencies:Ensure Sopel and OpenAI are ready:
pipx install sopel
pipx runpip sopel install openai



Configuration
To make the magic happen, you must configure Sopel’s default.cfg with the chat section, including your OpenAI API key and optional settings. Here’s the rundown:

Edit the Config:Open or create ~/.sopel/default.cfg:
nano ~/.sopel/default.cfg


Add Required Settings:Include the [core] and [chat] sections:
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
api_key = sk-...  # Your OpenAI API key (required)
model = gpt-4o-mini  # Model: gpt-3.5-turbo-0125, gpt-4-turbo-2024-04-09, gpt-4o-mini
history_limit = 50  # Max messages stored per channel
max_message_length = 450  # Max characters per IRC message
message_delay = 1.0  # Seconds between split messages

Important: Replace sk-... with your actual OpenAI API key from OpenAI. Without it, the bot will sulk like a crashed server.

Optional Settings:

model: Choose a different OpenAI model for more power (and cost).
history_limit: Adjust for longer/shorter conversation context.
max_message_length: Tweak for your IRC server’s limits.
message_delay: Increase if your server flags rapid messages as spam.


Save and Secure:Save the file and restrict permissions:
chmod 600 ~/.sopel/default.cfg



Usage

Launch Sopel:
sopel --config ~/.sopel/default.cfg


Chat with the Bot:Address the bot by its nick (e.g., ascii):

Ask a question:ascii: How do I secure my Linux server?

Response: “Lock it down with ufw, ditch root logins, and pray your users don’t sudo rm -rf /. Need a config walkthrough?”
Request a joke:ascii tell me a joke

Response: “Why do preppers love bash scripts? One cron job and your bunker’s stocked for the apocalypse!”
Clear history:ascii: reset

Response: “Conversation history wiped cleaner than a fresh Arch install!”


Commands:

Nick-Prefixed: ascii <message>, ascii: <message>, ascii, <message> (e.g., ascii debug my Python code).
Reset: .reset (channel-only, clears history).



Troubleshooting

Bot Not Responding:

Check logs:tail -f ~/.sopel/logs/sopel.log


Verify api_key is valid (test with OpenAI’s Python client).
Confirm chat plugin is loaded:.plugins




Generic or Off-Theme Responses:

Reset history to clear old context:ascii: reset


Ensure model in default.cfg supports your prompt (e.g., gpt-4o-mini).


Rate Limit Errors:

If you hit OpenAI’s limits (“rationing brainpower” message), wait 5 seconds or check your API quota at OpenAI.


Plugin Not Loading:

Verify ai-openai.py is in ~/.sopel/plugins/ and readable:ls -l ~/.sopel/plugins/ai-openai.py


Check plugins = chat in default.cfg.



Contributing
Want to beef up this bot’s bunker-ready skills? Fork, hack, and PR! Ideas:

Add a local joke cache to save API calls.
Implement ascii: debug <code> for code fixes.
Create a ascii: prepper tip for survival nuggets.

To contribute:

Fork and clone:git clone https://github.com/yourusername/sopel-ai-openai.git


Branch it:git checkout -b feature/epic-addition


Commit:git commit -m "Add epic feature"


Push and PR:git push origin feature/epic-addition



License
MIT License. See LICENSE for details.
Acknowledgments

Powered by Sopel and OpenAI.
Built for IRC warriors who live by the terminal and prep for the end of days.

