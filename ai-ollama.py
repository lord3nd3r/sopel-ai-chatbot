import requests
import logging
import threading
import json  # Ensure the json module is imported
from sopel import module
from sopel.config.types import StaticSection, ValidatedAttribute

logger = logging.getLogger(__name__)

# Configuration section for the plugin
class AIPluginSection(StaticSection):
    olama_server = ValidatedAttribute('olama_server', default='http://localhost:11434')
    llm_version = ValidatedAttribute('llm_version', default='rolandroland/llama3.1-uncensored')

def setup(bot):
    bot.config.define_section('ai_plugin', AIPluginSection)

def configure(config):
    config.define_section('ai_plugin', AIPluginSection)
    config.ai_plugin.olama_server = input('Enter the OLAMA server URL: ')
    config.ai_plugin.llm_version = input('Enter the LLM version: ')

@module.rule('^ai: (.*)')
def ai_response(bot, trigger):
    # Immediately acknowledge the user's command
    bot.say("Processing your request...")
    # Run the request in a separate thread to prevent blocking
    threading.Thread(target=process_ai_request, args=(bot, trigger)).start()

def process_ai_request(bot, trigger):
    query = trigger.group(1)
    try:
        response = get_ai_response(bot, query)
        chunks = split_into_chunks(response, 400)
        if len(chunks) > 1:
            bot.say(f"The response is lengthy and will be sent in {len(chunks)} parts.")
        for chunk in chunks:
            bot.say(chunk)
    except requests.exceptions.RequestException as e:
        logger.exception("Network error occurred while processing the request.")
        bot.say("Network error occurred while processing your request.")
    except ValueError as e:
        logger.exception("Error processing the response from the server.")
        bot.say("Error processing the response from the server.")
    except Exception as e:
        logger.exception("An unexpected error occurred.")
        bot.say("An unexpected error occurred while processing your request.")

def get_ai_response(bot, query):
    headers = {'Content-Type': 'application/json'}
    data = {
        'model': bot.config.ai_plugin.llm_version,
        'prompt': f'In 10000 characters or less, {query}'
    }

    # Set up a session with retries
    session = requests.Session()
    retries = requests.adapters.Retry(connect=3, backoff_factor=0.5)
    adapter = requests.adapters.HTTPAdapter(max_retries=retries)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    try:
        response = session.post(
            f"{bot.config.ai_plugin.olama_server}/api/generate",
            headers=headers,
            json=data,
            timeout=40  # seconds
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.exception("Error communicating with the OLAMA server.")
        raise

    response_text = ""
    content_type = response.headers.get('Content-Type', '')
    try:
        if 'application/json' in content_type:
            # If the response is a single JSON object
            response_json = response.json()
            response_text = response_json.get('response', '')
        else:
            # If the response is streamed
            for line in response.iter_lines():
                if line:
                    line_json = line.decode('utf-8')
                    response_json = json.loads(line_json)
                    if 'response' in response_json:
                        response_text += response_json['response']
    except ValueError as e:
        logger.exception("Error decoding the JSON response.")
        raise

    return response_text

def split_into_chunks(text, max_length):
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0
    for word in words:
        word_length = len(word) + 1  # Adding 1 for the space
        if current_length + word_length > max_length:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_length = len(word)
        else:
            current_chunk.append(word)
            current_length += word_length
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    return chunks
