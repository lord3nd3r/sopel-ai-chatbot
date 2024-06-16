import requests
import logging
import json  # Import the json module
from sopel import module

# Configuration for OLAMA server
OLAMA_SERVER = 'http://localhost:11434'
LLM_VERSION = 'llama2-uncensored'

logger = logging.getLogger(__name__)

@module.rule('^ai: (.*)')
def ai_response(bot, trigger):
    query = trigger.group(1)
    try:
        response = get_ai_response(query)
        for chunk in split_into_chunks(response, 400):
            bot.say(chunk)
    except Exception as e:
        logger.error(f"Error getting response from OLAMA: {e}")
        bot.say("Sorry, I couldn't process your request.")

def get_ai_response(query):
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        'model': LLM_VERSION,
        'prompt': f'In 700 characters or less, {query}'
    }
    response = requests.post(f"{OLAMA_SERVER}/api/generate", headers=headers, json=data, stream=True)
    
    if response.status_code != 200:
        logger.error(f"Error: Received status code {response.status_code} from OLAMA server")
        logger.error(f"Response: {response.text}")
        return "Sorry, there was an error communicating with the OLAMA server."

    response_text = ""
    try:
        for line in response.iter_lines():
            if line:
                line_json = line.decode('utf-8')
                response_json = json.loads(line_json)
                if 'response' in response_json:
                    response_text += response_json['response']
    except ValueError as e:
        logger.error(f"JSON decode error: {e}")
        return "Sorry, there was an error processing the response from the OLAMA server."

    return response_text

def split_into_chunks(text, max_length):
    words = text.split()
    chunks = []
    current_chunk = ""
    for word in words:
        if len(current_chunk) + len(word) + 1 > max_length:
            chunks.append(current_chunk.strip())
            current_chunk = word
        else:
            if current_chunk:
                current_chunk += " " + word
            else:
                current_chunk = word
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks
