from flask import Flask, request, jsonify
from langchain_community.llms import Ollama

app = Flask(__name__)
ollama = Ollama(model="llama3")

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get('prompt', '')
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    response_text = ollama.invoke(prompt)
    return jsonify({"response": response_text})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "OK"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
