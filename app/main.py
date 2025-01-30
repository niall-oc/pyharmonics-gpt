from .openai_handler import parse_args, query_openai, FUNCTION_ROUTER  # Import parse_args from the appropriate module
from flask import Flask, jsonify, request, render_template
import os
import yaml
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize Flask app
app = Flask(__name__)

prompt_context = yaml.safe_load(open("prompt_intent.yaml", "r"))
logging.debug(f"Loaded model context: {prompt_context}")

# Route to interact with OpenAI's GPT-3
@app.route('/query', methods=['POST'])
def query_openai_route():
    """
        Queries OpenAI's GPT* model to determine the how Pyharmonics API should be called.
        Calls the appropriate Pyharmonics API function and sends that response to OpenAI for further processing.
        Finally, returns the response from OpenAI to the client.
    """
    try:
        # Get JSON data from the request
        data = request.get_json()
        user_prompt = data.get('prompt')

        # User prompt isd required
        if not user_prompt:
            return jsonify({"error": "Prompt is required"}), 400

        # Determine the api call to make based on the user prompt
        function_name, args, kwargs = parse_args(
            query_openai(
                user_prompt,
                prompt_context['extract_args']
            )
        )

        # In this example we only want the user to interact with our Pyharmonics API.
        # If the user asks for something out of scope we explain to them what to ask first.
        # You may want to handle this differently in your application.
        if function_name not in FUNCTION_ROUTER:
            return jsonify({"response": prompt_context['extract_args_error']}), 200

        # Call the appropriate Pyharmonics API function and deal with any exceptions.
        symbol, interval = args
        try:
            harmonic_data = FUNCTION_ROUTER[function_name](symbol, interval, **kwargs)
            logging.info(f"Harmonic data: {harmonic_data.keys()}")
        except Exception as e:
            return jsonify({"response": f"Pyharmonics raised the following exception: {str(e)}"}), 200

        # Extract the plot and remove it from the harmonic data
        plot = harmonic_data.pop('plot', None)
        logging.info(f"harmonic data: {harmonic_data}")
        logging.info(f"base 64 image: {type(plot)}")

        # Prepare the response data. We only want to send the position or divergences to OpenAI.
        pyharmonics_response = str({
            "asset": symbol,
            "timeframe": interval,
            "found": harmonic_data.get('position', harmonic_data.get('divergences', {})),
        })
        logging.debug(f"Pyharmonics response is built as {type(pyharmonics_response)}\n{pyharmonics_response}")

        # Now we query OpenAI with the Pyharmonics response and the technical analysis context.
        model_response = query_openai(
            pyharmonics_response,
            prompt_context['technical_analysis']
        )
        logging.debug(f"OpenAI model response: {model_response}")

        # Return the OpenAI response with the Pyharmonics response and the plot
        response_data = {
            "response": {
                "model": model_response,
                "image": {
                    "data": plot,
                    "format": "image/png"
                }
            }
        }
        return jsonify(response_data), 200

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": f"{str(e)}"}), 500

@app.route('/')
def index():
    """
        Renders the chat UI.
    """
    return render_template('chat_ui.html')

if __name__ == "__main__":
    # Run the app on the host and port specified in environment variables
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
