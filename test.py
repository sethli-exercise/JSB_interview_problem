import flask_app
import ollama

def promptOllama(prompt: str):
    response = ollama.chat(
        model = 'llava',
        messages = [
            {'role '}])

def main():
    modelOutput = flask_app.run_ollama("How many parameters do you have?")
    print(modelOutput)
    return


if __name__ == "__main__":
    main()