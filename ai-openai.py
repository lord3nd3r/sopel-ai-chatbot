from sopel import plugin, config
from collections import deque
import openai
import logging
import time

# Set up logging
logger = logging.getLogger(__name__)

class ChatSection(config.types.StaticSection):
    api_key = config.types.SecretAttribute('api_key')
    model = config.types.ChoiceAttribute('model', choices=['gpt-3.5-turbo-0125', 'gpt-4-turbo-2024-04-09', 'gpt-4o-mini'], default='gpt-4o-mini')
    system_prompt = config.types.ValidatedAttribute('system_prompt', default='You are an IRC bot named {nick}. Respond in a friendly and helpful manner.')
    history_limit = config.types.ValidatedAttribute('history_limit', int, default=50)
    max_message_length = config.types.ValidatedAttribute('max_message_length', int, default=450)
    message_delay = config.types.ValidatedAttribute('message_delay', float, default=1.0)

def setup(bot):
    bot.config.define_section('chat', ChatSection)
    if not bot.config.chat.api_key:
        raise config.ConfigurationError('OpenAI API key is required in [chat] section.')
    bot.memory['openai_client'] = openai.OpenAI(api_key=bot.config.chat.api_key)
    bot.memory['message_history'] = {}  # Clear any existing history
    logger.info("AI-OpenAI plugin setup complete.")

def send_response(bot, channel, text, max_length=450, delay=1.0):
    """Split long responses into multiple messages and send with a delay."""
    parts = []
    while text:
        if len(text) <= max_length:
            parts.append(text)
            break
        split_at = text.rfind(' ', 0, max_length)  # Split at last space within limit
        if split_at == -1:
            split_at = max_length  # Force split if no space found
        parts.append(text[:split_at])
        text = text[split_at:].lstrip()
    
    # Send each part with a delay
    for i, part in enumerate(parts):
        bot.say(part, channel)
        if i < len(parts) - 1:  # Delay only between messages
            time.sleep(delay)

@plugin.event('PRIVMSG')
@plugin.rule('.*')
def handle_message(bot, trigger):
    channel = trigger.sender
    nick = trigger.nick
    text = trigger.group(0)

    # Log the incoming message for debugging
    logger.debug(f"Received message in {channel} from {nick}: {text}")

    # Respond if the message starts with the bot's nickname followed by a space
    if not text.lower().startswith(bot.nick.lower() + ' '):
        logger.debug(f"Message ignored: does not start with '{bot.nick.lower()} '")
        return

    # Initialize message history for the channel
    if channel not in bot.memory['message_history']:
        bot.memory['message_history'][channel] = deque(maxlen=bot.config.chat.history_limit)
    bot.memory['message_history'][channel].append((nick, text))

    # Prepare messages with system prompt and history
    system_prompt = bot.config.chat.system_prompt.format(nick=bot.nick) if bot.config.chat.system_prompt else ''
    system_prompt += ' Do not include your name or any prefix in your responses.'  # Explicit instruction
    messages = [{'role': 'system', 'content': system_prompt}] if system_prompt else []
    for sender, msg in bot.memory['message_history'][channel]:
        role = 'assistant' if sender == bot.nick else 'user'
        messages.append({'role': role, 'content': msg})  # Use raw message content without sender prefix

    try:
        logger.debug(f"Sending OpenAI request with model {bot.config.chat.model}")
        response = bot.memory['openai_client'].chat.completions.create(
            model=bot.config.chat.model,
            messages=messages
        )
        if response.choices:
            response_text = response.choices[0].message.content.strip()
            if response_text:
                logger.debug(f"Received response: {response_text[:100]}...")  # Log first 100 chars
                send_response(bot, channel, response_text, bot.config.chat.max_message_length, bot.config.chat.message_delay)
                bot.memory['message_history'][channel].append((bot.nick, response_text))
            else:
                logger.warning("Empty response from OpenAI API.")
                bot.say('I got an empty response. Try asking again?', channel)
        else:
            logger.warning("No response choices from OpenAI API.")
            bot.say('Hmm, I didn’t get a response from the AI. Try again?', channel)
    except Exception as e:
        logger.error(f'Error generating response: {e}')
        bot.say(f'Sorry, something went wrong: {e}', channel)
