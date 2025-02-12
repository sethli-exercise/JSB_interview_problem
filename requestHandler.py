import tempfile
import streamlit as st

import llmInterface
import speechToText
import textToSpeech

class RequestHandler:
    def __init__(self, ollamaInterface: llmInterface.LLMInterface, speech: textToSpeech.TextToSpeech, stt: speechToText.SpeechToText):
        self.llmInterface = ollamaInterface
        self.speech = speech
        self.stt = stt

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

    def promptForm(self):

        # form for submitting prompts to the LLM
        with (st.form(key="inputPrompt", clear_on_submit=True)):
            # audio input ##############################################################################################
            audio = st.audio_input("Say something.")
            submitAudio = st.form_submit_button("Submit Recording.")
            if audio and submitAudio:
                print("audio exists",audio)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tempAudio:
                    tempAudio.write(audio.getvalue())
                    tempAudioPath = tempAudio.name
                text = self.stt.transcribeFile(tempAudioPath)

                st.session_state.displayedMessages.append(text)

                llmResponse = self.llmInterface.promptModel(text)
                # print(llmResponse)
                st.session_state.displayedMessages.append(llmResponse)

            # typed input ##############################################################################################
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

    def playbackForm(self):
        with (st.form(key="playback")):
            playback = st.form_submit_button("Playback Last Response")
            volumeSliderVal = st.slider("Volume", 0.01, 1.0, 0.5)
            stopPlayback = st.form_submit_button("Stop Playback")
            self.speech.setVolume(volumeSliderVal)

            if playback:
                self.speech.speakText(st.session_state.displayedMessages[-1])

            if stopPlayback:
                self.speech.stop()

    def mainPage(self):

        st.title('Fantastic Hallucinations from LLMs')

        self.promptForm()

        self.playbackForm()

        # holds conversation history
        with st.container():
            self.displayMessages(st.session_state.displayedMessages)
            # print(st.session_state.displayedMessages)
            # print("########################")
