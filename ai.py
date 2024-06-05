import requests
import logging
from sopel import module

API_KEY = 'your_openai_api_key_here'
API_URL = 'https://api.openai.com/v1/chat/completions'
MODEL = 'gpt-3.5-turbo'

logger = logging.getLogger(__name__)

@module.rule('^ai: (.*)')
def chatgpt_response(bot, trigger):
    query = trigger.group(1)
    try:
        response = get_chatgpt_response(query)
        for chunk in split_into_chunks(response, 400):
            bot.say(chunk)
    except Exception as e:
        logger.error(f"Error getting response from ChatGPT: {e}")
        bot.say("Sorry, I couldn't process your request.")

def get_chatgpt_response(query):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}',
    }
    data = {
        'model': MODEL,
        'messages': [
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': f'In 700 characters or less, {query}'}
        ],
        'max_tokens': 150,
        'temperature': 0.7,
    }
    response = requests.post(API_URL, headers=headers, json=data)
    
    if response.status_code == 429:
        logger.error(f"Error: Received status code 429 from OpenAI API")
        logger.error(f"Response: {response.text}")
        return "Sorry, it looks like we've hit the usage limit. Please try again later."

    if response.status_code != 200:
        logger.error(f"Error: Received status code {response.status_code} from OpenAI API")
        logger.error(f"Response: {response.text}")
        return "Sorry, there was an error communicating with the OpenAI API."

    response_json = response.json()
    
    if 'choices' not in response_json:
        logger.error(f"Unexpected response format: {response_json}")
        return "Sorry, there was an error processing the response from the OpenAI API."
    
    return response_json['choices'][0]['message']['content']

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
