# app/api/routes.py
from flask import Blueprint, request, jsonify
from .pyharmonics_handler import whats_new_binance, whats_forming_binance, parse_args
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path='../../.vscode/.env')

os.getenv("OPENAI_API_KEY")

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
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # Or the engine you are using
            messages=[
                {
                    "role": "developer",
                    "content": """You are generating parameters for an python API.
                    Parameters: symbol, interval, candles=, limit_to=, percent_complete=.
                    Symbol means the stock or crypto symbol, crypto uses forming-binance, stocks use forming-yahoo.
                    Interval means the timeframe, 15m, 1h, 4h, 1d, 1w are supported.
                    candles means the number of candles to analyze, default is 1000.
                    limit_to means the last number candles where the pattern completion is to be checked, default is 10.
                    percent_complete is a float means how much of the final leg of price movement is completed, default is 0.8.
                    Only respond with an exact json string repesenting args kwargs for the function.
                    Do not pad the json string with any `"` or `'` characters.
                    """
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=100
        )
        args, kwargs = parse_args(response.choices[0].message.content)
        symbol, interval = args

        response_data = whats_forming_binance(symbol, interval, **kwargs)
        # Return the detected patterns
        input = str({
            "asset": symbol,
            "timeframe": interval,
            "found": response_data
        })

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Or the engine you are using
            messages=[
                {
                    "role": "developer",
                    "content": """You are a trading bot that is analyzing the harmonics forming in a given asset and timeframe.
                    You are going to explain what price to buy or sell at, and what patterns are forming.
                    The input is a json string containing the asset, timeframe, and the found patterns.
                    Be concise and clear in your response.
                    """
                },
                {"role": "user", "content": input}
            ],
            max_tokens=100
        )

        # Return the OpenAI response
        return jsonify({"response": f"{response.choices[0].message.content} \n {response_data}"}), 200

    except Exception as e:
        return jsonify({"error": f"{str(e)}"}), 500
