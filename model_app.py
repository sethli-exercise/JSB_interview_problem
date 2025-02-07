import subprocess

import flask_app
import streamlit_app

class semiPersistantModel:
    # special delimiter used by the model so it can differentiate between prompts
    __delimiter = "&&&&**(%"

    def __init__(self, model: str):
        self.model = model
        self.conversationHistory = [f"Only respond to the last prompt the rest are the previous prompts. Each prompt is delimited by {semiPersistantModel.__delimiter}"]

    #
    def conversationHistoryToStr(self):
        return semiPersistantModel.__delimiter.join(prompt for prompt in self.conversationHistory)

    #
    def promptModel(self, prompt):
        self.conversationHistory.append(prompt)
        conversationConcat = self.conversationHistoryToStr()



def main():
    flask_app.main()
    streamlit_app.main()


if __name__ == "__main__":
    main()