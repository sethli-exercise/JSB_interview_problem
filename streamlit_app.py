import sys
import time

import streamlit as st
import requests
import signal

import textToSpeech
import llmInterface
import requestHandler

def main():
    speech = textToSpeech.TextToSpeech()
    interface = llmInterface.LLMInterface(model = "mistral")
    frontEndServer = requestHandler.RequestHandler(interface, speech)
    frontEndServer.mainPage()

if __name__ == "__main__":
    main()