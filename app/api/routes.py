# app/api/routes.py
from flask import Blueprint, request, jsonify
from .pyharmonics_handler import whats_new_binance, whats_forming_binance
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI API with the API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

# Create a Flask Blueprint for routes
api_blueprint = Blueprint('api', __name__)


@api_blueprint.route('/formed-binance', methods=['POST'])
def formed_b():
    """
    Route to analyze the harmonics formed in a given asset and timeframe
    """
    try:
        # Get JSON data from the request
        data = request.get_json()
        symbol = data.get('symbol')
        interval = data.get('interval')
        candles = data.get('candles') or 1000
        limit_to = data.get('limit_to') or -1

        # Check if asset and timeframe are provided
        if not symbol or not interval:
            return jsonify({"error": f"Symbol and interval are required. Data was {data}"}), 400

        # Call the pyharmonics API to analyze the asset and timeframe
        response_data = whats_new_binance(symbol, interval, limit_to=int(limit_to), candles=int(candles))

        # Return the detected patterns
        return jsonify({
            "asset": symbol,
            "timeframe": interval,
            "found": response_data
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_blueprint.route('/forming-binance', methods=['POST'])
def forming_b():
    """
    Route to analyze the harmonics formed in a given asset and timeframe
    """
    try:
        # Get JSON data from the request
        data = request.get_json()
        symbol = data.get('symbol')
        interval = data.get('interval')
        candles = data.get('candles') or 1000
        limit_to = data.get('limit_to') or -1
        percent_complete = data.get('percent_complete') or 0.8

        # Check if asset and timeframe are provided
        if not symbol or not interval:
            return jsonify({"error": f"Symbol and interval are required. Data was {data}"}), 400

        # Call the pyharmonics API to analyze the asset and timeframe
        response_data = whats_forming_binance(symbol, interval, limit_to=int(limit_to), candles=int(candles), percent_complete=float(percent_complete))

        # Return the detected patterns
        return jsonify({
            "asset": symbol,
            "timeframe": interval,
            "found": response_data
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Route to interact with OpenAI's GPT-3
@api_blueprint.route('/query-openai', methods=['POST'])
def query_openai_route():
    try:
        # Get JSON data from the request
        data = request.get_json()
        prompt = data.get('prompt')

        # Ensure a prompt is provided
        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        # Use OpenAI's API to generate a response
        response = openai.Completion.create(
            engine="text-davinci-003",  # Or the engine you are using
            prompt=prompt,
            max_tokens=100
        )

        # Return the OpenAI response
        return jsonify({"response": response.choices[0].text.strip()}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
