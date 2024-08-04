from flask import Flask, request, jsonify
import requests
import json
from ai_bot import AIBot
ai_bot = AIBot()

app = Flask(__name__)

OLLAMA_HOST = "localhost"  # Change this to localhost if running locally
OLLAMA_PORT = "11434"
def call_ollama(prompt):
    try:
        response = requests.post(f"http://{OLLAMA_HOST}:{OLLAMA_PORT}/api/generate", json={"model": "llama3", "prompt": prompt})
        response.raise_for_status()  # Check for HTTP errors
        print("Raw Response:", response.text)  # Debug: Print raw response
        result = response.json()  # Attempt to parse the JSON response
        return result.get("response", "Error: No response generated")
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        return "Error: Failed to parse response from the AI model."
    except requests.exceptions.RequestException as e:
        print(f"Failed to connect to Ollama API: {e}")
        return "Error: Failed to generate a response from the AI model."


@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get('prompt', '')
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    
    response_text = call_ollama(prompt)
    return jsonify({"response": response_text})

@app.route('/select_question_type', methods=['POST'])
def process_question():
    data = request.json
    question_type = data.get('type', '').strip()

    if question_type == "random":
        # Logic for generating a random question
        case_synopsis = data.get('case_synopsis', '').strip()
        if not case_synopsis:
            return jsonify({"error": "No case synopsis provided"}), 400
        
        # Use the AI bot to generate a random question based on the case synopsis
        question = ai_bot.generate_random_question(case_synopsis)
        return jsonify({"question": question})

    elif question_type == "manual":
        # Logic for processing a manual question input
        question = data.get('question', '').strip()
        if not question:
            return jsonify({"error": "No question provided"}), 400
        return jsonify({"question": question})

    else:
        return jsonify({"error": "Invalid question type"}), 400

@app.route('/select_action', methods=['POST'])
def select_action():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    choice = data.get('choice', '').strip()

    if choice == "1":
        return jsonify({"action": "Ask a question"})
    elif choice == "2":
        return jsonify({"action": "Make a final decision"})
    elif choice == "3":
        return jsonify({"action": "Exit"})
    else:
        return jsonify({"error": "Invalid choice"}), 400

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "OK"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
