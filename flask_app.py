from flask import Flask, jsonify, request
import threading
import logging
import subprocess
import sys
import model_app

app = Flask(__name__)

# List to store messages
messages = []

stt = subprocess.Popen(["streamlit", "run" ,"streamlit_app.py"])

def input_thread():
    model = model_app.semiPersistentModel("mistral")

    while True:
        prompt = input("Provide a prompt for llava or enter QUIT to exit the program:\n")

        if prompt == "QUIT":
            exit(0)

        # prompt the model with the given input
        modelOutput = model.promptModel(prompt)
        messages.append(["user's prompt", prompt])
        messages.append(["LLM response:", modelOutput])


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