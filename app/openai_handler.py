# Description: This module contains the functions for handling OpenAI API requests.
from .pyharmonics_handler import whats_forming_binance, whats_forming_yahoo, whats_options_interest, whats_options_volume
import openai
import json
import logging

# Map the function names to the actual functions
FUNCTION_ROUTER = {
    "forming_binance": whats_forming_binance,
    "forming_yahoo": whats_forming_yahoo,
    "options_interest": whats_options_interest,
    "options_volume": whats_options_volume
}

def parse_args(string):
    """
        Parses the given string into Python variables.

        Args:
            string: The string to be parsed.

        Returns:
            A tuple containing the parsed args and kwargs.
    """
    try:
        data = json.loads(string)
        logging.info(f"Data: {data}")
        function_name = data.get('function_name', '')
        args = data.get('args', [])
        kwargs = data.get('kwargs', {})
        logging.info(f"preparing to call {function_name}({args}, {kwargs})")
        return function_name, args, kwargs
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON string: {string}")
    except Exception as e:
        print(f"Error: {e}")
    return None, None, None


def query_openai(prompt, developer_content, model='gpt-3.5-turbo'):
    """
        Determines the intent of the given prompt.

        Args:
            prompt: The prompt to be analyzed.

        Returns:
            A tuple containing the function name, args, and kwargs.
    """
    logging.debug(f"Prompt: {prompt}")
    logging.debug(f"Developer content: {developer_content}")
    logging.debug(f"Model: {model}")
    response = openai.ChatCompletion.create(
        model=model,  # An economical model for testing and development.
        messages=[
            {"role": "developer", "content": developer_content},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100
    )
    return response.choices[0].message.content
