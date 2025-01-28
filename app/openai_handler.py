# Description: This module contains the functions for handling OpenAI API requests.
from .pyharmonics_handler import whats_forming_binance, whats_forming_yahoo, whats_options_interest, whats_options_volume
from openai import OpenAI
import json
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai_api_model = os.getenv("OPENAI_API_MODEL")  # Ensure the OpenAI API model is set
openai_api_base_url = os.getenv("OPENAI_API_BASE_URL")  # Ensure the OpenAI API base URL is set
logging.info(f"OpenAI - API model: {openai_api_model}, base URL: {openai_api_base_url}")

# Map the function names to the actual functions
FUNCTION_ROUTER = {
    "forming_binance": whats_forming_binance,
    "forming_yahoo": whats_forming_yahoo,
    "options_interest": whats_options_interest,
    "options_volume": whats_options_volume
}

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=openai_api_base_url
)

def parse_args(string):
    """
        Parses the given string into Python variables.

        Args:
            string: The openai response string to be parsed and converted into Python variables.
        Returns:
            A tuple containing the parsed function name, args and kwargs.
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


def query_openai(prompt, developer_content, model=None):
    """
        Determines the intent of the given prompt.

        Args:
            prompt: The user prompt to be analyzed.
            developer_content: The developer content to be sent to OpenAI.
            model: The model to be used for the OpenAI API call. Defaults to the environment variable model if not provided.
        Returns:
            A string containing the response from OpenAI or an error message.
    """
    logging.debug(f"Prompt: {prompt}")
    logging.debug(f"Developer content: {developer_content}")
    logging.debug(f"Model: {model}")
    try:
        response = client.chat.completions.create(
            model=model or openai_api_model,
            messages=[
                {"role": "developer", "content": developer_content},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error: {e}")
        return f"Error: {e}"
