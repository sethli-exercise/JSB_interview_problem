import tempfile
import streamlit as st
import datetime

import llmInterface
import pdfTextExtract
import speechToText
import textToSpeech

class RequestHandler:

    __KEY_USER_PROMPT = "User's Prompt:"
    __KEY_LLM_RESPONSE = "LLM's Response:"
    __KEY_DATETIME_START =  "start"
    __KEY_DATETIME_FINISH = "finish"

    def __init__(self, ollamaInterface: llmInterface.LLMInterface, speech: textToSpeech.TextToSpeech, stt: speechToText.SpeechToText, pdfReader: pdfTextExtract.PDFTextExtract):
        self.llmInterface = ollamaInterface
        self.speech = speech
        self.stt = stt
        self.pdfReader = pdfReader

        if "displayedMessages" not in st.session_state:
            st.session_state.displayedMessages = []
        if "playbackVolume" not in st.session_state:
            st.session_state.playbackVolume = 0.5
        return

    # render the entire conversation history between the user and the LLM
    def displayMessages(self, messages: list):
        for i in range(len(messages)):

            timeDiff = messages[i][RequestHandler.__KEY_DATETIME_FINISH] - messages[i][RequestHandler.__KEY_DATETIME_START]
            st.markdown(f"Took about {timeDiff.total_seconds()} seconds")

            st.markdown(RequestHandler.__KEY_USER_PROMPT + " #" + str(i + 1))
            st.info(messages[i][RequestHandler.__KEY_USER_PROMPT])

            st.markdown(RequestHandler.__KEY_LLM_RESPONSE)
            playback = st.button("Playback#" + str(i + 1))
            if playback:
                self.speech.speakText(messages[i][RequestHandler.__KEY_LLM_RESPONSE])
            st.warning(messages[i][RequestHandler.__KEY_LLM_RESPONSE]) # st.warning() is used b/c it has a different background color to st.info()

            # st.divider()

    def addConversationEntry(self, prompt: str, llmResponse: str, start, finish):

        conversationEntry = \
            {
                RequestHandler.__KEY_USER_PROMPT: prompt,
                RequestHandler.__KEY_LLM_RESPONSE: llmResponse,
                RequestHandler.__KEY_DATETIME_START: start,
                RequestHandler.__KEY_DATETIME_FINISH: finish
            }
        # print(len(st.session_state.displayedMessages))
        st.session_state.displayedMessages.append(conversationEntry)
        # print(len(st.session_state.displayedMessages))

    # listen to the user to capture a recording
    # then use the whisper model to transcribe the text
    def chatInput(self):
        audio = st.audio_input("Say something.")
        submitAudio = st.form_submit_button("Submit Recording.")
        if audio and submitAudio:
            # print("audio exists", audio)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tempAudio:
                tempAudio.write(audio.getvalue())
                tempAudioPath = tempAudio.name
            prompt = self.stt.transcribeFile(tempAudioPath)

            # submit the transcribed audio to the LLM
            startTime = datetime.datetime.now()
            llmResponse = self.llmInterface.promptModel(prompt)
            finishTime = datetime.datetime.now()

            self.addConversationEntry(prompt, llmResponse, startTime, finishTime)

    def ragInput(self):

        prompt = st.text_input("What would you like to ask?", "Enter your prompt here.")

        col1, col2 = st.columns([1,3])
        with col1:
            submitFile = st.form_submit_button("Upload File")
        with col2:
            file = st.file_uploader("Upload pdf", type="pdf")

        # submit button for form
        submitted = st.form_submit_button("Submit")
        if submitted:
            # submit the typed prompt to the LLM
            startTime = datetime.datetime.now()

            llmResponse = ""
            if file is not None :
                pdfText = self.pdfReader.extractText(file.read())
                llmResponse = self.llmInterface.promptModel(prompt + pdfText)
            else:
                llmResponse = self.llmInterface.promptModel(prompt)

            finishTime = datetime.datetime.now()

            self.addConversationEntry(prompt, llmResponse, startTime, finishTime)

    def typeInput(self):
        prompt = st.text_input("What would you like to ask?", "Enter your prompt here.")

        # submit button for form
        submitted = st.form_submit_button("Submit")
        if submitted:
            # submit the typed prompt to the LLM
            startTime = datetime.datetime.now()
            llmResponse = self.llmInterface.promptModel(prompt)
            finishTime = datetime.datetime.now()

            self.addConversationEntry(prompt, llmResponse, startTime, finishTime)

    def inputOption(self) -> str:
        inputOption = st.radio(
            "inputOptions",
            [
                "CHAT",
                "RAG",
                "TYPE"
            ],
            captions=
            [
                "Verbal input to LLM",
                "Text input to LLM with files",
                "Text input to LLM"
            ],
            label_visibility= "hidden"
        )

        return inputOption

    def promptForm(self,inputOption: str):

        # form for submitting prompts to the LLM
        with (st.form(key="inputPrompt", clear_on_submit=True)):

            # display the corresponding input form
            if inputOption == "CHAT":
                self.chatInput()
            elif inputOption == "RAG":
                self.ragInput()
            elif inputOption == "TYPE":
                self.typeInput()
            else:
                st.write("Select an Option")

    def playbackForm(self):
        with (st.form(key="playback")):
            # col1, col2 = st.columns([1, 1])
            # with col1:
            st.write("Playback Settings")
            volumeSliderVal = st.slider("Volume", 0.01, 1.0, 0.5)
            self.speech.setVolume(volumeSliderVal)
            # with col2:
            stopPlayback = st.form_submit_button("Stop Playback")
            if stopPlayback:
                self.speech.stop()

    def mainPage(self):

        st.title('Fantastic Hallucinations from LLMs')

        col1, col2 = st.columns([3, 1])
        with col1:
            inputOption = self.inputOption()
        with col2:
            self.playbackForm()

        self.promptForm(inputOption)

        # holds conversation history
        with st.container():
            self.displayMessages(st.session_state.displayedMessages)
            # print(st.session_state.displayedMessages)
            # print("########################")
