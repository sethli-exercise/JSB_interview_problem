import subprocess

import flask_app
import streamlit_app


# function from chatgpt
def run_ollama(prompt: str, model: str="llava"):
    try:
        # Run the Ollama CLI command
        result = subprocess.run(
            ["ollama", "run", model, "--prompt", prompt],
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


def main():
    flask_app.main()
    streamlit_app.main()
    while True:

        prompt = input("Provide a prompt for llava or enter QUIT to exit the program:\n")

        if prompt == "QUIT":
            return

        
