import sys
import time

import streamlit as st
import requests
import signal

import pdfTextExtract
import textToSpeech
import llmInterface
import requestHandler
import speechToText

def main():

    # models tried:
    # llama3.3, llava, llama2-uncensored
    # mistral, gemma
    interface = llmInterface.LLMInterface(model = "mistral")
    stt = speechToText.SpeechToText()
    speech = textToSpeech.TextToSpeech()
    pdfReader = pdfTextExtract.PDFTextExtract()
    frontEndServer = requestHandler.RequestHandler(interface, speech, stt, pdfReader)
    frontEndServer.mainPage()

if __name__ == "__main__":
    main()

# TODO save conversation history as text file

# test mistral and mistral instruct are the same

# test mistral on other pdfs and websites

# test llava for single image with diff gestures/objects

# report latency for all parts of application

#################################################

# pdf summary of implementation