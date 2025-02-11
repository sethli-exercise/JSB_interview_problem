import streamlit as st
import llmInterface

class RequestHandler:
    def __init__(self, llmInterface: llmInterface.LLMInterface):
        self.llmInterface = llmInterface

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
