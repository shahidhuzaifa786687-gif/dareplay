from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import random

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Load questions
with open("questions.json", "r") as file:
    data = json.load(file)


@app.route("/")
def home():
    """Serve the main HTML page"""
    return render_template("index.html")


@app.route("/api/question", methods=["GET"])
def get_question():
    """Get a random question based on difficulty and choice"""
    difficulty = request.args.get("difficulty", "kids")
    choice = request.args.get("choice", "truth")
    
    # Validate inputs
    if difficulty not in data:
        return jsonify({"error": "Invalid category. Choose: kids or adult"}), 400
    
    if choice not in data[difficulty]:
        return jsonify({"error": "Invalid choice. Choose: truth or dare"}), 400
    
    questions = data[difficulty].get(choice, [])
    
    if not questions:
        return jsonify({"error": "No questions available"}), 404
    
    question = random.choice(questions)
    
    return jsonify({
        "question": question,
        "difficulty": difficulty,
        "choice": choice
    }), 200


@app.route("/api/difficulties", methods=["GET"])
def get_difficulties():
    """Get all available difficulty levels"""
    difficulties = list(data.keys())
    return jsonify({"difficulties": difficulties}), 200


@app.route("/api/choices", methods=["GET"])
def get_choices():
    """Get all available choices (truth/dare)"""
    difficulty = request.args.get("difficulty", "kids")
    
    if difficulty not in data:
        return jsonify({"error": "Invalid difficulty"}), 400
    
    choices = list(data[difficulty].keys())
    return jsonify({"choices": choices}), 200


@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    # when running directly, enable debug only if FLASK_ENV=development
    debug_mode = app.config.get("DEBUG", False)
    app.run(debug=debug_mode, host="0.0.0.0", port=5000)
