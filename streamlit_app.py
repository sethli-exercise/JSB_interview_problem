import sys
import time

import streamlit as st
import requests
import signal

import llmInterface
import requestHandler

def main():
    interface = llmInterface.LLMInterface(model = "mistral")
    frontEndServer = requestHandler.RequestHandler(interface)
    frontEndServer.mainPage()

if __name__ == "__main__":
    main()