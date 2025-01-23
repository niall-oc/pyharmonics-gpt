from .openai_handler import parse_args, query_openai, FUNCTION_ROUTER  # Import parse_args from the appropriate module
from flask import Flask, jsonify, request, render_template
from dotenv import load_dotenv
import os
import yaml
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")  # Ensure the OpenAI API key is set
openai_api_model = os.getenv("OPENAI_API_MODEL")  # Ensure the OpenAI API model is set
logging.info(f"OpenAI API model: {openai_api_model}")

# Initialize Flask app
app = Flask(__name__)

gpt_prompt_intent = yaml.safe_load(open("gpt_prompt_intent.yaml", "r"))
logging.debug(f"Loaded GPT-3 prompt intents: {gpt_prompt_intent}")

# Route to interact with OpenAI's GPT-3
@app.route('/query', methods=['POST'])
def query_openai_route():
    try:
        # Get JSON data from the request
        data = request.get_json()
        prompt = data.get('prompt')

        # Ensure a prompt is provided
        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        # Determine the intent of the prompt
        function_name, args, kwargs = parse_args(query_openai(prompt, gpt_prompt_intent['extract_args'], model=openai_api_model))

        if function_name not in FUNCTION_ROUTER:
            return jsonify({"response": gpt_prompt_intent['extract_args_error']}), 200

        # Call the appropriate function
        symbol, interval = args
        try:
            harmonic_data = FUNCTION_ROUTER[function_name](symbol, interval, **kwargs)
            logging.info(f"Harmonic data: {harmonic_data.keys()}")
        except Exception as e:
            return jsonify({"response": f"Pyharmonics raised the following exception: {str(e)}"}), 200

        # Prepare the response data
        pyharmonics_response = str({
            "asset": symbol,
            "timeframe": interval,
            "found": harmonic_data
        })

        # Get the response from OpenAI
        response = query_openai(pyharmonics_response, gpt_prompt_intent['technical_analysis'], model=openai_api_model)

        # Return the OpenAI response
        return jsonify({"response": f"{response}"}), 200

    except Exception as e:
        return jsonify({"error": f"{str(e)}"}), 500

@app.route('/')
def index():
    return render_template('chat_ui.html')

if __name__ == "__main__":
    # Run the app on the host and port specified in environment variables
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
