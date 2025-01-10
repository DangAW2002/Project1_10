from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from scr.app_logging import configure_logger, state_logger, error_logger
from scr.timeout_guard import timeout_guard
from scr.state import user_assistant_prompt
from app import run_conversation, reset_chat, gradio_interface

app = Flask(__name__)
CORS(app)  # Add this line to enable CORS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_conversation', methods=['POST'])
def api_run_conversation():
    message = request.json['message']
    print(f"Received message: {message}")
    response = gradio_interface(message, "")
    print(f"Response: {response}")
    return jsonify({'response': response})

@app.route('/reset', methods=['POST'])
def api_reset():
    reset_chat()
    return jsonify({'message': 'Chat has been reset.'})

if __name__ == "__main__":
    configure_logger()
    print("Starting Flask server...")  # Add this line
    app.run(host="0.0.0.0", port=5000)