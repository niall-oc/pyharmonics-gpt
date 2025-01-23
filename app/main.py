from flask import Flask, jsonify
from app.api.routes import api_blueprint  # Import routes
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Register the API blueprint
app.register_blueprint(api_blueprint)


# Root endpoint
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Harmonics + OpenAI API!"}), 200


if __name__ == "__main__":
    # Run the app on the host and port specified in environment variables
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
