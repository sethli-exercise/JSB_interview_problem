import ollama

class LLMInterface:
    # special delimiter used by the model so it can differentiate between prompts
    __delimiter = "&&&&**(%"

    def __init__(self, model: str="llama3.3"):
        self.model = model
        # initialize the context of the conversation
        self.conversationHistory = [f"Only respond to the last prompt the rest are the previous prompts. Look at the previous prompts for context.Each prompt is delimited by {LLMInterface.__delimiter}"]

    # format the list of prompts into one string
    def conversationHistoryToStr(self):
        return LLMInterface.__delimiter.join(prompt for prompt in self.conversationHistory)

    # prompts the model with the parameter prompt
    # also provides the model with the past conversation history
    def promptModel(self, prompt):
        self.conversationHistory.append(prompt)
        conversationConcat = self.conversationHistoryToStr()
        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    'role': 'user',
                    'content': conversationConcat
                }
            ]
        )

        return response['message']['content']
