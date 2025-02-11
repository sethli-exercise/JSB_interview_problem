import streamlit as st
import llmInterface
import textToSpeech

class RequestHandler:
    def __init__(self, ollamaInterface: llmInterface.LLMInterface, speech: textToSpeech.TextToSpeech):
        self.llmInterface = ollamaInterface
        self.speech = speech

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
            listening = st.toggle("Speech to Text")

            if listening:
                x = None #TODO convert the speech to text then fill in prompt with it

            # submit button for form
            submitted = st.form_submit_button("Submit")
            if submitted:
                # print("sent prompt")
                st.session_state.displayedMessages.append(prompt)

                llmResponse = self.llmInterface.promptModel(prompt)
                # print(llmResponse)
                st.session_state.displayedMessages.append(llmResponse)

        with (st.form(key="Playback")):
            playback = st.form_submit_button("Playback Last Response")
            volumeSliderVal = st.slider("Volume", 0.01, 1.0, 0.5)
            stopPlayback = st.form_submit_button("Stop Playback")
            self.speech.setVolume(volumeSliderVal)

            if playback:
                self.speech.speakText(st.session_state.displayedMessages[-1])

            if stopPlayback:
                self.speech.stop()



        # holds conversation history
        with st.container():
            self.displayMessages(st.session_state.displayedMessages)
            # print(st.session_state.displayedMessages)
            # print("########################")
