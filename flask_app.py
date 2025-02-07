from flask import Flask, jsonify, request
import threading
import logging
import subprocess
import sys

app = Flask(__name__)

# List to store messages
messages = []

stt = subprocess.Popen(["streamlit", "run", "streamlit_app.py"])

# function from chatgpt
def run_ollama(prompt: str, model: str="llava"):
    try:
        subprocess.run(["ollama serve"])

        # Run the Ollama CLI command
        result = subprocess.run(
            ["ollama run", model, "--prompt", prompt],
            text=True,  # Return the output as a string
            capture_output=True  # Capture stdout and stderr
        )
        # Check if the command was successful
        if result.returncode == 0:
            return result.stdout
        else:
            raise Exception(f"Error: {result.stderr}")
    except FileNotFoundError:
        return "Ollama CLI is not installed or not found in your PATH."
    except Exception as e:
        return str(e)

def input_thread():
    while True:
        prompt = input("Provide a prompt for llava or enter QUIT to exit the program:\n")

        if prompt == "QUIT":
            return

        modelOutput = run_ollama(prompt)
        messages.append(prompt)
        messages.append(modelOutput)


@app.route('/get_messages', methods=['GET'])
def get_messages():
    return jsonify({"messages": messages})

@app.route('/send_message', methods = ['POST'])
def send_message():
    data = request.json["messages"]
    messages.append(data)
    return

def main():
    try:

        # Starting a thread for terminal input to not block the Flask app
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.WARNING)

        thread = threading.Thread(target=input_thread)
        thread.daemon = True
        thread.start()

        # Starting Flask app
        app.run(port=5000)

    except KeyboardInterrupt:
        stt.terminate()
        sys.exit(0)

if __name__ == '__main__':
    main()