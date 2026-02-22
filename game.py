from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import random
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Load questions from the same directory as this script so the app still works
# when the current working directory is different (e.g. under gunicorn).
base_dir = os.path.dirname(os.path.abspath(__file__))
questions_path = os.path.join(base_dir, "questions.json")

try:
    with open(questions_path, "r") as file:
        data = json.load(file)
except Exception as e:
    # if loading fails, log and exit; the app can't function without questions
    raise RuntimeError(f"failed to load questions.json: {e}")


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




@app.route("/api/players", methods=["POST"])
def pick_player():
    """Choose a random player from a posted list.

    Expects JSON `{"names": ["Alice","Bob", ...]}` with between 2 and 4
    non-empty strings.  Returns `{ "selected": "Bob" }` on success or an
    error message with an appropriate status code.
    """
    payload = request.get_json(silent=True)
    if not payload or "names" not in payload:
        return jsonify({"error": "JSON with 'names' array required"}), 400

    names = payload.get("names")
    if not isinstance(names, list):
        return jsonify({"error": "'names' must be an array"}), 400

    # strip and filter empty strings
    cleaned = [n.strip() for n in names if isinstance(n, str) and n.strip()]
    if len(cleaned) < 2 or len(cleaned) > 4:
        return jsonify({"error": "Provide between 2 and 4 player names"}), 400

    selected = random.choice(cleaned)
    return jsonify({"selected": selected}), 200


@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    # when running directly, enable debug only if FLASK_ENV=development
    debug_mode = app.config.get("DEBUG", False)
    app.run(debug=debug_mode, host="0.0.0.0", port=5000)
    @app.route("/privacy")
    def privacy():
     return render_template("privacy.html")

    @app.route("/terms")
    def terms():
     return render_template("terms.html")