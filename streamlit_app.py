import sys
import time

import streamlit as st
import requests
import signal

import textToSpeech
import llmInterface
import requestHandler
import speechToText

def main():
    speech = textToSpeech.TextToSpeech()
    interface = llmInterface.LLMInterface(model = "mistral")
    stt = speechToText.SpeechToText()
    frontEndServer = requestHandler.RequestHandler(interface, speech, stt)
    frontEndServer.mainPage()

if __name__ == "__main__":
    main()