import ollama

conversation = ["Only respond to the last prompt the rest are the previous prompts. Each prompt is delimited by &&&&**(%."]

def testJoin(string: str):
    conversation.append(string)
    conversationString = "&&&&**(%".join(entry for entry in conversation)
    print(conversationString)

def promptOllama(prompt: str, model: str):
    conversation.append(prompt)
    conversationString = "&&&&**(%".join(entry for entry in conversation)

    response = ollama.chat(
        model = model,
        messages = [
            {'role': 'user',
             'content': conversationString
             }
        ]
    )
    return response

def test1():
    modelVersion = "llama3.3"
    # modelOutput = flask_app.run_ollama("How many parameters do you have?")
    modelOutput = promptOllama("write bananas", modelVersion)
    print(modelOutput['message']['content'])

    modelOutput = promptOllama("what is the last prompt you were given", modelVersion)
    print(modelOutput['message']['content'])
    return

def test2():
    testJoin("message 1")
    testJoin("message 2")


def main():
    test1()


if __name__ == "__main__":
    main()



