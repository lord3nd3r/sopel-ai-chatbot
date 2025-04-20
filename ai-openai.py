from sopel import plugin, config
from collections import deque
import openai
import logging
import time
import re
from openai import OpenAIError, RateLimitError, AuthenticationError

# Set up logging
logger = logging.getLogger(__name__)

class ChatSection(config.types.StaticSection):
    api_key = config.types.SecretAttribute('api_key')
    model = config.types.ChoiceAttribute('model', choices=['gpt-3.5-turbo-0125', 'gpt-4-turbo-2024-04-09', 'gpt-4o-mini'], default='gpt-4o-mini')
    system_prompt = config.types.ValidatedAttribute('system_prompt', default='You are a highly knowledgeable AI with the personality of a Linux expert, hardcore prepper, and skilled developer, acting as an encyclopedia of all human knowledge. You provide accurate, detailed, and practical answers with a rugged, self-reliant mindset, offering survival tips, coding solutions, or Linux command-line wizardry. Your responses are infused with sharp, witty humor, making complex topics engaging and fun. When asked for a joke, deliver a short, punchy joke tied to Linux, programming, or prepping, avoiding generic humor. Stay concise unless elaboration is requested, and prioritize actionable advice. Whether debugging code, building a bunker, or explaining quantum physics, you’re confident, clear, and playfully sarcastic.')
    history_limit = config.types.ValidatedAttribute('history_limit', int, default=50)
    max_message_length = config.types.ValidatedAttribute('max_message_length', int, default=450)
    message_delay = config.types.ValidatedAttribute('message_delay', float, default=1.0)

def setup(bot):
    bot.config.define_section('chat', ChatSection)
    if not bot.config.chat.api_key:
        raise config.ConfigurationError('OpenAI API key is required in [chat] section.')
    bot.memory['openai_client'] = openai.OpenAI(api_key=bot.config.chat.api_key)
    bot.memory['message_history'] = {}
    bot.memory['last_request'] = {}  # Track last request time per channel
    logger.info("AI-OpenAI plugin setup complete.")

def send_response(bot, channel, text, max_length=450, delay=1.0):
    parts = []
    while text:
        if len(text) <= max_length:
            parts.append(text)
            break
        split_at = text.rfind(' ', 0, max_length)
        if split_at == -1:
            parts.append(text[:max_length] + '...')
            text = text[max_length:]
        else:
            parts.append(text[:split_at])
            text = text[split_at:].lstrip()
    
    for i, part in enumerate(parts):
        bot.say(part, channel)
        if i < len(parts) - 1:
            time.sleep(delay)
    if len(parts) > 1 and len(text) > max_length:
        bot.say("Response truncated. Ask for details if needed!", channel)

@plugin.event('PRIVMSG')
@plugin.rule('.*')
@plugin.priority('high')
def handle_message(bot, trigger):
    channel = trigger.sender
    nick = trigger.nick
    text = trigger.group(0)

    # Check for bot nick followed by space, colon, or comma
    pattern = re.compile(rf'^{re.escape(bot.nick)}(\s+|[:,]\s+)(.*)', re.IGNORECASE)
    match = pattern.match(text)
    if not match:
        logger.debug(f"Message ignored: does not match pattern for '{bot.nick}'")
        return
    user_message = match.group(2).strip()
    logger.debug(f"Received message in {channel} from {nick}: {user_message}")

    # Rate limiting: 1 request per 5 seconds per channel
    current_time = time.time()
    last_request = bot.memory['last_request'].get(channel, 0)
    if current_time - last_request < 5:
        logger.debug(f"Rate limit hit for {channel}")
        bot.say("Whoa, slow down! I'm still compiling the last response.", channel)
        return
    bot.memory['last_request'][channel] = current_time

    # Initialize message history for the channel
    if channel not in bot.memory['message_history']:
        bot.memory['message_history'][channel] = deque(maxlen=bot.config.chat.history_limit)
    bot.memory['message_history'][channel].append((nick, user_message))

    # Prepare system prompt
    system_prompt = bot.config.chat.system_prompt
    if system_prompt:
        try:
            system_prompt = system_prompt.format(nick=bot.nick)
        except KeyError:
            logger.warning("System prompt formatting failed; using raw prompt.")
    
    # If the message is a joke request, reinforce the theme
    if user_message.lower().startswith('tell me a joke'):
        system_prompt += ' When asked for a joke, tell a short, witty joke related to Linux, programming, or prepping, keeping your rugged, humorous personality.'
    
    system_prompt += ' Do not include your name or any prefix in your responses.'
    messages = [{'role': 'system', 'content': system_prompt}] if system_prompt else []
    for sender, msg in bot.memory['message_history'][channel]:
        role = 'assistant' if sender == bot.nick else 'user'
        messages.append({'role': role, 'content': msg})

    try:
        logger.debug(f"Sending OpenAI request with model {bot.config.chat.model}")
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f"OpenAI messages: {messages}")
        response = bot.memory['openai_client'].chat.completions.create(
            model=bot.config.chat.model,
            messages=messages
        )
        if response.choices:
            response_text = response.choices[0].message.content.strip()
            if response_text:
                logger.debug(f"Received response: {response_text[:100]}...")
                send_response(bot, channel, response_text, bot.config.chat.max_message_length, bot.config.chat.message_delay)
                bot.memory['message_history'][channel].append((bot.nick, response_text))
            else:
                logger.warning("Empty response from OpenAI API.")
                bot.say("My joke generator's out of RAM. Try again?", channel)
        else:
            logger.warning("No response choices from OpenAI API.")
            bot.say("The AI's too busy debugging its own code. Try again?", channel)
    except RateLimitError:
        logger.error("OpenAI rate limit exceeded.")
        bot.say("The AI's rationing its brainpower like I ration MREs. Try again soon!", channel)
    except AuthenticationError:
        logger.error("OpenAI API key invalid.")
        bot.say("My API key's gone AWOL. Yell at the admin!", channel)
    except OpenAIError as e:
        logger.error(f"OpenAI error: {e}")
        bot.say(f"AI hiccup: {e}. Try again?", channel)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        bot.say(f"Something broke like a bad script in prod: {e}. Retry?", channel)

@plugin.command('reset')
@plugin.require_chanmsg
def reset_history(bot, trigger):
    channel = trigger.sender
    if channel in bot.memory['message_history']:
        bot.memory['message_history'][channel].clear()
        bot.say("Conversation history wiped cleaner than a fresh Arch install!", channel)
    else:
        bot.say("No history to reset. We're already off-grid!", channel)
