import sys
import time

import streamlit as st
import requests
import signal

import ollama

class LLMInterface:
    # special delimiter used by the model so it can differentiate between prompts
    __delimiter = "&&&&**(%"

    def __init__(self, model: str="llama3.3"):
        self.model = model
        # initialize the context of the conversation
        self.conversationHistory = [f"Only respond to the last prompt the rest are the previous prompts. Each prompt is delimited by {LLMInterface.__delimiter}"]

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


def sigterm_handler(signum, frame):
    sys.exit(0)

class FrontEndServer():
    def __init__(self):
        self.llmInterface = LLMInterface(model="llava")

        # displayed messages must be stored in the session_state otherwise it will be re-initialized when the web app updates
        if "displayedMessages" not in st.session_state:
            st.session_state.displayedMessages = []
        return

    # render the entire conversation history between the user and the LLM
    def displayMessages(self, messages: list):
        for i in range(len(messages)):
            if i % 2 == 0:
                st.markdown("User's Prompt:")
            else:
                st.markdown("LLM's Response:")

            st.info(messages[i])
            st.divider()

    def mainPage(self):

        st.title('Fantastic Hallucinations from LLMs')

        # form for submitting prompts to the LLM
        with (st.form(key="inputPrompt", clear_on_submit=True)):
            # text input for form
            prompt = st.text_input("What would you like to ask?", "Enter your prompt here.")

            # submit button for form
            submitted = st.form_submit_button("Submit")
            if submitted:
                # print("sent prompt")
                st.session_state.displayedMessages.append(prompt)

                llmResponse = self.llmInterface.promptModel(prompt)
                # print(llmResponse)
                st.session_state.displayedMessages.append(llmResponse)

        # holds conversation history
        with st.container():
            self.displayMessages(st.session_state.displayedMessages)
            # print(st.session_state.displayedMessages)
            # print("########################")

# render the entire conversation history between the user and the LLM
def displayMessages(messages: list):
    for i in range(len(messages)):
        if i % 2 == 0:
            st.markdown("User's Prompt:")
        else:
            st.markdown("LLM's Response:")

        st.info(messages[i])
        st.divider()

def main():
    frontEndServer = FrontEndServer()
    frontEndServer.mainPage()

if __name__ == "__main__":
    main()