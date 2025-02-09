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


# signal.signal(signal.SIGTERM, sigterm_handler)

# def fetch_messages():
#     try:
#         response = requests.get('http://localhost:5000/get_messages')
#         if response.status_code == 200:
#             return response.json()["messages"]
#         else:
#             return []
#     except Exception as e:
#         st.error(f"Failed to fetch messages: {str(e)}")
#         return []
#
# def send_message(message: str):
#     url = 'http://localhost:5000/send_message'
#     data = {
#         "msg": message
#     }
#
#     try:
#         response = requests.post(url, json = data)
#         if response.status_code == 200:
#             return response.json()
#         else:
#             return response.json()["messages"]
#     except Exception as e:
#         st.error(f"failed to send message: {str(e)}")
#         return []


def displayMessages(messages):
    for message in messages:
        # st.markdown(message[0])
        st.info(message)
        st.divider()




def main():
    st.session_state.displayedMessages = []
    llmInterface = LLMInterface(model = "llava")


    st.title('Fantastic Hallucinations from LLMs')
    with (st.form(key = "inputPrompt", clear_on_submit=True)):
        prompt = st.text_input("What would you like to ask?", "Enter your prompt here.")

        # submit button
        submitted = st.form_submit_button("Submit")
        if submitted:
            print("sent prompt")
            st.session_state.displayedMessages.append(prompt)
            llmResponse = llmInterface.promptModel(prompt)
            print(llmResponse)
            st.session_state.displayedMessages.append(llmResponse)

    with st.container():
        displayMessages(st.session_state.displayedMessages)


        # st.write(prompt)

    # st.markdown("<span style='color: blue;'>This text is blue!</span>", unsafe_allow_html=True)

    # displayedMessages = []
    # while True:
    #     # time.sleep(1000)
    #     messages = fetch_messages()
    #     new_messages = [msg for msg in messages if msg not in displayedMessages]
    #
    #     if new_messages:
    #         display_messages(new_messages)
    #         displayedMessages.extend(new_messages)
    #     st.rerun()

if __name__ == "__main__":
    main()