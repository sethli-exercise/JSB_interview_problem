import ollama

class LLMInterface:
    # special delimiter used by the model so it can differentiate between prompts
    __delimiter = "&&&&**(%"

    def __init__(self, model: str="llama3.3"):
        self.model = model
        # initialize the context of the conversation
        self.conversationHistory = [
            {"role": "system", "content": "You are a helpful AI assistant."}
        ]

    # format the list of prompts into one string
    # def conversationHistoryToStr(self):
    #     return LLMInterface.__delimiter.join(prompt for prompt in self.conversationHistory)

    # prompts the model with the parameter prompt
    # also provides the model with the past conversation history
    def promptModel(self, prompt, imageBytes = None):
        # self.conversationHistory.append(prompt)
        # print(len(self.conversationHistory))

        # format the newest prompt for the model
        message = {
                'role': 'user',
                'content': prompt
            }


        if imageBytes is not None:
            # print("adding image to message")
            message['images'] = [imageBytes]

        # add the newest prompt to the history
        self.conversationHistory.append(message)

        response = ollama.chat(
            model=self.model,
            messages=self.conversationHistory
        )

        self.conversationHistory.append({"role": "assistant", "content": response['message']['content']})

        return response['message']['content']
